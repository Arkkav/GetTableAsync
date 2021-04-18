import aiohttp
import asyncio
import logging
import os
# from client_volume import config


# DEBUG = True															# Debug or error level for a logger messages
# SERVER_ADDRESS = 'localhost'  #'0.0.0.0'    # 'get_table_server-instance'  #											# The address we are listening to
# SERVER_PORT = '8000'  													# Port
# LOGGER_NAME = 'get_table_client'										# The name of our logger
# LOG_FILE_PATH = os.environ['PWD'] + '/client_volume'
# ROWS_NUMBER_LIST = '1,10,100'.split(',')

DEBUG = os.environ['DEBUG']																# Debug or error level for a logger messages
SERVER_ADDRESS = os.environ['SERVER_ADDRESS']   #'0.0.0.0'  #'localhost'  											# The address we are listening to
SERVER_PORT = os.environ['SERVER_PORT']   													# Port
LOGGER_NAME = os.environ['LOGGER_NAME']											# The name of our logger
LOG_FILE_PATH = os.environ['LOG_FILE_PATH']
ROWS_NUMBER_LIST = os.environ['ROWS_NUMBER_LIST'].split(',')


def logging_configure(debug_level):
    logger = logging.getLogger(LOGGER_NAME)
    # Logger format with level, time and message
    formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(message)s')
    file_handler = logging.FileHandler(LOG_FILE_PATH + '/log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(debug_level)
    aiohttp_logger = logging.root.manager.loggerDict['aiohttp.client']
    for hdlr in aiohttp_logger.handlers[:]:
        if isinstance(hdlr, (logging.FileHandler, logging.StreamHandler)):
            aiohttp_logger.removeHandler(hdlr)
    aiohttp_logger.addHandler(file_handler)
    aiohttp_logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
    return logger


api_logger = logging_configure(logging.DEBUG if DEBUG else logging.WARNING)


async def on_request_start(session, context, params):
    logging.getLogger('aiohttp.client').debug(f'Starting request <{params.url, params.method, params.headers}>')


async def get_rows(url, session, params):
    async with session.get(url, params=params) as response:
        logging.getLogger('aiohttp.client').debug(f'Response: <{response.url}>')
        logging.getLogger('aiohttp.client').debug(f'{str(response.headers)}')
        logging.getLogger('aiohttp.client').debug(f'<{await response.text()}>')


async def run(rows):
    url = 'http://' + SERVER_ADDRESS + ':' + str(SERVER_PORT) + '/'
    tasks = []
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        for i in rows:
            params = {'n': str(i)}
            params = '?' + ''.join([k + '=' + v for k, v in params.items()])
            task = asyncio.create_task(get_rows(url + params, session, {}))
            tasks.append(task)
        return await asyncio.gather(*tasks)

asyncio.run(run(ROWS_NUMBER_LIST))




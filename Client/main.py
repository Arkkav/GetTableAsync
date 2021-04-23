import aiohttp
import asyncio
import logging
import os


DEBUG = bool(os.environ['DEBUG'])									# Debug or error level for a logger messages
SERVER_ADDRESS = os.environ['SERVER_ADDRESS']   					# The address we are listening to
SERVER_PORT = os.environ['SERVER_PORT']   							# Port
LOGGER_NAME = os.environ['LOGGER_NAME']								# The name of our logger
LOG_FILE_PATH = os.environ['LOG_FILE_PATH']                         # Path for log in the container
ROWS_NUMBER_LIST = os.environ['ROWS_NUMBER_LIST'].split(',')        # Number of times and rows to get from server


def logging_configure(debug_level):
    logger = logging.getLogger(LOGGER_NAME)
    # Logger format with level, time and message
    formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(message)s')
    file_handler = logging.FileHandler(LOG_FILE_PATH + '/log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(debug_level)
    # setup http requests log
    aiohttp_logger = logging.root.manager.loggerDict['aiohttp.client']
    for hdlr in aiohttp_logger.handlers[:]:
        if isinstance(hdlr, (logging.FileHandler, logging.StreamHandler)):
            aiohttp_logger.removeHandler(hdlr)
    aiohttp_logger.addHandler(file_handler)
    aiohttp_logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
    return logger

# Global logger variable
api_logger = logging_configure(logging.DEBUG if DEBUG else logging.WARNING)


async def on_request_start(session, context, params):
    # coroutine for tracing responses (starts in a proper time)
    logging.getLogger('aiohttp.client').debug(f'Starting request <{params.url, params.method, params.headers}>')


async def get_rows(url, session, params):
    try:
        async with session.get(url, params=params) as response:
            logging.getLogger('aiohttp.client').debug(f'Response: <{response.method} {response.status} {response.url}>')
            logging.getLogger('aiohttp.client').debug(f'{str(response.headers)}')
            logging.getLogger('aiohttp.client').debug(f'<{await response.text()}>')
    except aiohttp.ClientConnectorError as e:
        api_logger.debug(str(e))
    except asyncio.TimeoutError as e:
        api_logger.debug('TimeoutError')
    except aiohttp.ClientOSError as e:
        api_logger.debug(str(e))
    except aiohttp.ServerDisconnectedError as e:
        api_logger.debug(str(e))


async def run(rows):
    url = 'http://' + SERVER_ADDRESS + ':' + str(SERVER_PORT) + '/'    # form URL
    tasks = []
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    timeout = aiohttp.ClientTimeout(total=400)
    async with aiohttp.ClientSession(trace_configs=[trace_config], timeout=timeout) as session:
        for i in rows:
            params = {'n': str(i)}
            # form parameters string from scratch because I want
            # to get them in on_request_start for tracing properly
            params = '?' + ''.join([k + '=' + v for k, v in params.items()])
            task = asyncio.create_task(get_rows(url + params, session, {}))         # create tasks from coroutines
            tasks.append(task)
        return await asyncio.gather(*tasks)                         # collect all tasks, run and get results


if __name__ == '__main__':
    asyncio.run(run(ROWS_NUMBER_LIST))

import aiohttp
import asyncio
import logging
import config


def logging_configure(debug_level):
    logger = logging.getLogger(config.LOGGER_NAME)
    # Logger format with level, time and message
    formatter: logging.Formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(message)s')
    handler = logging.FileHandler(config.LOG_FILE_NAME)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(debug_level)
    aiohttp_logger = logging.root.manager.loggerDict['aiohttp.client']
    for hdlr in aiohttp_logger.handlers[:]:
        if isinstance(hdlr, logging.FileHandler):
            aiohttp_logger.removeHandler(hdlr)
    aiohttp_logger.addHandler(handler)
    aiohttp_logger.setLevel(logging.DEBUG if config.DEBUG else logging.WARNING)
    return logger


api_logger = logging_configure(logging.DEBUG if config.DEBUG else logging.WARNING)


async def on_request_start(session, context, params):
    logging.getLogger('aiohttp.client').debug(f'Starting request <{params.url, params.method, params.headers}>')


async def get_rows(url, session, params):
    async with session.get(url, params=params) as response:
        logging.getLogger('aiohttp.client').debug(f'Response: <{response.url}>')
        logging.getLogger('aiohttp.client').debug(f'{str(response.headers)}')
        logging.getLogger('aiohttp.client').debug(f'<{await response.text()}>')


async def run(rows):
    url = 'http://' + config.SERVER_ADDRESS + ':' + str(config.SERVER_PORT) + '/'
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

asyncio.run(run(config.ROWS_NUMBER_LIST))




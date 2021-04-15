from aiohttp import web
import pandas as pd
import json
import config
import logging


def logging_configure(debug_level):
    logger = logging.getLogger(config.LOGGER_NAME)
    # Logger format with level, time and message
    formatter: logging.Formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(message)s')
    # handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    handler = logging.FileHandler(config.LOG_FILE_NAME)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(debug_level)
    aiohttp_logger = logging.root.manager.loggerDict['aiohttp.access']
    for hdlr in aiohttp_logger.handlers[:]:
        if isinstance(hdlr, logging.FileHandler):
            aiohttp_logger.removeHandler(hdlr)
    aiohttp_logger.addHandler(handler)
    aiohttp_logger.setLevel(logging.DEBUG if config.DEBUG else logging.WARNING)
    return logger


api_logger = logging_configure(logging.DEBUG if config.DEBUG else logging.WARNING)


def error_json(message):
    api_logger.debug(message)
    raise web.HTTPBadRequest(body=json.dumps({'Error': message}).encode())


class Handler:
    def __init__(self):
        self.df = pd.read_csv(config.CSV_URL)

    async def all_handler(self, request):
        if request.method == 'GET':
            params = request.rel_url.query
            n = params.get('n', None)
            if not n:
                error_json('Parameter n should be defined as integer.')
            try:
                n = int(n)
            except (ValueError, TypeError) as e:
                error_json('Parameter n should be defined as integer.')
            return web.json_response(self.df.head(n=n).to_dict())
        else:
            message = 'Method not allowed.'
            data = {'Error': message}
            api_logger.debug(message)
            raise web.HTTPMethodNotAllowed(request.method, allowed_methods=['GET'], body=json.dumps(data).encode())

    async def not_found_handler(self, request):
        message = "Resource '{resourse}' not found.".format(resourse=request.match_info.get('name', ''))
        data = {'Error': message}
        api_logger.debug(message)
        raise web.HTTPNotFound(body=json.dumps(data).encode())


def web_app(argv):
    app = web.Application()
    handler = Handler()
    app.add_routes([
        web.get('/{name}', handler.not_found_handler),
        web.route('*', '/', handler.all_handler),
    ])
    return app


if __name__ == '__main__':
    web.run_app(web_app(''), host=config.SERVER_ADDRESS, port=config.SERVER_PORT)

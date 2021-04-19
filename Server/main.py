from aiohttp import web
import pandas as pd
import numpy as np
import json
import logging
import os
import sys


# DEBUG = True															# Debug or error level for a logger messages
# SERVER_ADDRESS = 'localhost'  											# The address we are listening to
# SERVER_PORT = 8000  													# Port
# LOGGER_NAME = 'get_table_server'										# The name of our logger
# LOG_FILE_PATH = os.environ['PWD'] + '/server_volume'
# CSV_URL = r'https://stepik.org/media/attachments/course/4852/StudentsPerformance.csv'

DEBUG = os.environ['DEBUG']															# Debug or error level for a logger messages
SERVER_ADDRESS = os.environ['SERVER_ADDRESS'] 											# The address we are listening to
SERVER_PORT = os.environ['SERVER_PORT']  													# Port
LOGGER_NAME = os.environ['LOGGER_NAME']										# The name of our logger
LOG_FILE_PATH = os.environ['LOG_FILE_PATH']
CSV_URL = os.environ['CSV_URL']


def logging_configure(debug_level):
    logger = logging.getLogger(LOGGER_NAME)
    # Logger format with level, time and message
    formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(message)s')
    file_handler = logging.FileHandler(LOG_FILE_PATH + '/log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(debug_level)
    aiohttp_logger = logging.root.manager.loggerDict['aiohttp.access']
    # for hdlr in aiohttp_logger.handlers[:]:
    #     if isinstance(hdlr, (logging.FileHandler, logging.StreamHandler)):
    #         aiohttp_logger.removeHandler(hdlr)
    # aiohttp_logger.addHandler(file_handler)
    aiohttp_logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
    return logger


api_logger = logging_configure(logging.DEBUG if DEBUG else logging.WARNING)


def error_json(message):
    api_logger.debug(message)
    raise web.HTTPBadRequest(body=json.dumps({'Error': message}).encode())


class Handler:
    def __init__(self, read_df):
        self.df = read_df()

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

    @staticmethod
    async def not_found_handler(request):
        message = "Resource '{resourse}' not found.".format(resourse=request.match_info.get('name', ''))
        data = {'Error': message}
        api_logger.debug(message)
        raise web.HTTPNotFound(body=json.dumps(data).encode())


def students_performance_csv_to_df():
    dtype = {
        'math score': np.int8,
        'reading score': np.int8,
        'writing score': np.int8,
    }
    df = pd.read_csv(CSV_URL, dtype=dtype)
    category_cols = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
    df[category_cols] = df[category_cols].astype('category')
    return df


def web_app(argv):
    app = web.Application()
    handler = Handler(students_performance_csv_to_df)
    app.add_routes([
        web.get('/{name}', handler.not_found_handler),
        web.route('*', '/', handler.all_handler),
    ])
    return app


if __name__ == '__main__':
    web.run_app(web_app(''), host=SERVER_ADDRESS, port=int(SERVER_PORT), access_log=api_logger,
                access_log_format='"%r" %s %b "%{Referer}i" "%{User-Agent}i"')
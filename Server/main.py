from aiohttp import web
import asyncio
import pandas as pd
import json


class Handler:
    def __init__(self):
        self.df = pd.read_csv(r'https://stepik.org/media/attachments/course/4852/StudentsPerformance.csv')

    async def all_handler(self, request):
        if request.method == 'GET':
            params = request.rel_url.query
            n = params.get('n', None)
            if not n:
                data = {'Error': 'Parameter n should be defined as integer.'}
                raise web.HTTPBadRequest(body=json.dumps(data).encode())
            try:
                n = int(n)
            except (ValueError, TypeError) as e:
                data = {'Error': 'Parameter n should be defined as integer.'}
                raise web.HTTPBadRequest(body=json.dumps(data).encode())
            return web.json_response(self.df.head(n=n).to_dict())
        else:
            data = {'Error': 'Method not allowed.'}
            raise web.HTTPMethodNotAllowed(request.method, allowed_methods=['GET'], body=json.dumps(data).encode())

    async def not_found_handler(self, request):
        data = {'Error': "Resource '{resourse}' not found.".format(resourse=request.match_info.get('name', ''))}
        raise web.HTTPMethodNotAllowed(request.method, allowed_methods=['GET'], body=json.dumps(data).encode())


def web_app(argv):
    app = web.Application()
    handler = Handler()
    app.add_routes([
        web.get('/{name}', handler.not_found_handler),
        web.route('*', '/', handler.all_handler),
    ])
    return app


if __name__ == '__main__':
    web.run_app(web_app(''))

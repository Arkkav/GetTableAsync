from aiohttp import web
import asyncio
import pandas as pd


class Handler:
    def __init__(self):
        pass

    async def handle_get(self, request):
        request
        data = {'some': 'data'}
        return web.json_response(data)
        # return web.Response(text="Hello, world")


def init_func(argv):
    app = web.Application()
    handler = Handler()
    app.add_routes([web.get('/', handler.handle_get),
                    web.get('/', handler.handle_get),
                    ])
    return app


if __name__ == '__main__':
    web.run_app(init_func(''))

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

async def handle(request):
	return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
	web.run_app(app, host='127.0.0.1', port=9000)

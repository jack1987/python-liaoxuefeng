from aiohttp import web
import asyncio

routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    await asyncio.sleep(2)
    return web.json_response({
        'name': 'index'
    })


@routes.get('/about')
async def about(request):
    await asyncio.sleep(0.5)
    return web.Response(text="<h1>about us</h1>")

async def hello(request):
    await asyncio.sleep(0.5)
    ## here how to get query parameters
    #http://localhost:8080/hello?name=Jack&age=3
    param1 = request.rel_url.query['name']
    param2 = request.rel_url.query['age']
    result = "name: {}, age: {}".format(param1, param2)
    return web.Response(text=str(result))

def init():
    app = web.Application()
    app.add_routes(routes)
    app.router.add_route('GET', "/hello", hello)
    web.run_app(app)


init()

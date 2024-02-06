from aiohttp import web

routes = web.RouteTableDef()

app = web.Application()

app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000)

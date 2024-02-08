
import socketio
from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response
from loggate import getLogger, setup_logging

from config import get_config
from libs.helper import get_yaml

# from libs.socket_manager import SocketManager

logging_profiles = get_yaml(get_config('LOGGING_DEFINITIONS'))
setup_logging(profiles=logging_profiles)

logger = getLogger(__name__)

app = web.Application(logger=getLogger('iohttp'))
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins='*',
    engineio_logger=getLogger('socketio')
)
sio.attach(app) #, socketio_path='/backend/socket.io')
# routes = web.RouteTableDef()

#
async def on_prepare(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'


@sio.on('*')
async def any_event(event, sid, data):
    logger.info('topic %s %s: %s', event, sid, data)
    await sio.emit(
        'counter',
        [{'op': 'add', 'path': '/foo', 'value': {'id': 1, 'name': 'XXX'}}]
    )

# @routes.get(r'/ws/')
# async def init_socket(request: Request) -> Response:
#     print('*'*80)
#     return await app['msocket'].websocket_handler(request)



# app.add_routes(routes)
# app['msocket'] = SocketManager()


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000, access_log=None)

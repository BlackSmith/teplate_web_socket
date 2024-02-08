
import socketio
from socketio.exceptions import ConnectionRefusedError
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
    namespaces=['/', '/admin'],
    engineio_logger=getLogger('socketio')
)
sio.attach(app) #, socketio_path='/backend/socket.io')
# routes = web.RouteTableDef()

#
async def on_prepare(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'


@sio.on('connect', namespace='/user')
async def admin_connect(sid, environ, auth):
    if auth['username'] != 'admin':
        raise ConnectionRefusedError('authentication failed')
    async with sio.session(sid, namespace='/user') as session:
        session['username'] = auth['username']

@sio.on('reset', namespace='/user')
async def reset(sid, data):
    logger.error(data)
    async with sio.session(sid, '/user') as session:
        logger.info('%s: %s', session['username'], data)
    await sio.emit(
        'counter',
        [{'op': 'add', 'path': '/user', 'value': {'id': 1, 'name': 'XXX'}}]
    )

@sio.on('topic', namespace='/')
async def topic(sid, data):
    logger.info('topic %s: %s', sid, data)
    await sio.emit(
        'counter',
        [{'op': 'add', 'path': '/foo', 'value': {'id': 1, 'name': 'XXX'}}]
    )



# app.add_routes(routes)
# app['msocket'] = SocketManager()


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000, access_log=None)

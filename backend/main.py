
import socketio
from socketio.exceptions import ConnectionRefusedError
from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from loggate import getLogger, setup_logging

from config import get_config
from general_socket import GeneralSocketDispatcher
from libs.helper import get_yaml
from private_socket import PrivateSocketDispatcher

# from libs.socket_manager import SocketManager

logging_profiles = get_yaml(get_config('LOGGING_DEFINITIONS'))
setup_logging(profiles=logging_profiles)

logger = getLogger(__name__)

db_engine = create_async_engine(get_config('DB_URI'))
# db_session = async_sessionmaker(bind=db_engine)

app = web.Application(logger=getLogger('iohttp'))
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins='*',
    namespaces=['/', '/private'],
    engineio_logger=getLogger('socketio')
)
sio.attach(app) #, socketio_path='/backend/socket.io')
sio.register_namespace(GeneralSocketDispatcher(db_engine))
sio.register_namespace(PrivateSocketDispatcher(db_engine))

# routes = web.RouteTableDef()

#
async def on_prepare(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000, access_log=None)

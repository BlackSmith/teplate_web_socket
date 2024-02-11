import socketio
from loggate import getLogger
from sqlalchemy.ext.asyncio import AsyncEngine

logger = getLogger(__name__)


class PrivateSocketDispatcher(socketio.AsyncNamespace):
    """
    Handlers for anonymous users
    """

    def __init__(self, db_engine: AsyncEngine):
        super().__init__('/private')
        self.db_engine = db_engine

    async def on_connect(self, sid, environ, auth):
        if (not auth or auth['username'] != 'admin' or
                auth['password'] != 'passwd'):
            logger.error('authentication failed')
            return False
            # raise ConnectionRefusedError('authentication failed')
        logger.info(f'A new private user {auth["username"]} {sid} '
                    f'({environ["REMOTE_ADDR"]}) is connected.')
        # we save user IP to local session
        async with self.session(sid) as session:
            session['ip'] = environ["REMOTE_ADDR"]
            session['username'] = auth['username']
        await self.enter_room(sid, 'private_room')
        # Send init data
        await self.emit(
            'files',
            [{'op': 'add', 'path': '/private.txt',
              'value': {'id': 100, 'size': 12345}}]
        )

    async def on_disconnect(self, sid):
        async with self.session(sid) as session:
            user = session.get('username', '')
            ip = session.get('ip', '')
            logger.info(f'The user {user} {sid} ({ip}) is disconnected.')
        await self.leave_room(sid, 'private_room')

    # async def load_collection(self, collecton, session, sid):
    #     stmt = select(file_table).limit(30)
    #     async with self.db_engine.connect() as db:
    #         files = await db.execute(stmt)
    #         res = []
    #         await self.emit('images', [{'op': 'add', 'path': f'/{collecton}', 'value': []}])
    #         for ix, file in enumerate(files.fetchall()):
    #             file = File(**{str(key): getattr(file, key) for key in files.keys()})
    #             res.append({
    #                 'op': 'add',
    #                 'path': f'/{collecton}/{ix}',
    #                 'value': file.to_json()
    #               })
    #         await self.emit('files', res)

    async def on_private_topic(self, sid, data):
        print(f'Received private topic {sid}: {data}')
        await self.emit(
            'files',
            [{'op': 'add', 'path': '/private2.txt',
              'value': {'id': 2, 'size': 456}}]
        )

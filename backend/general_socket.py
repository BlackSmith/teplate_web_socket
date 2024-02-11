import socketio
from loggate import getLogger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from db_schema import file_table
from models.file import File

logger = getLogger(__name__)


class GeneralSocketDispatcher(socketio.AsyncNamespace):
    """
    Handlers for anonymous users
    """

    def __init__(self, db_engine: AsyncEngine):
        super().__init__('/')
        self.db_engine = db_engine

    async def on_connect(self, sid, environ):
        logger.info(f'New user {sid} ({environ["REMOTE_ADDR"]}) connected.')
        # we save user IP to local session
        async with self.session(sid) as session:
            session['ip'] = environ["REMOTE_ADDR"]
            # Send init data
            await self.emit(
            'files',
            [{'op': 'add', 'path': '/foo.txt', 'value': {'id': 1, 'size': 12345}}]
            )
            # await self.load_collection('D', session, sid)
        await self.enter_room(sid, 'default_room')

    async def on_disconnect(self, sid):
        async with self.session(sid) as session:
            ip = session['ip']
        logger.info(f'New user {sid} ({ip}) connected.')
        await self.leave_room(sid, 'default_room')

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

    async def on_topic(self, sid, data):
        print(f'Received topic {sid}: {data}')
        await self.emit(
            'files',
            [{'op': 'add', 'path': '/foo2.txt', 'value': {'id': 2, 'size': 456}}]
        )

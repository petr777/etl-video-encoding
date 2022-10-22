from aiobotocore.session import AioSession
from contextlib import AsyncExitStack
from settings import settings


class AioVK:

    def __init__(self):
        self._exit_stack = AsyncExitStack()

    async def __aenter__(self, session: AioSession = AioSession()):
        vk_session = session.create_client(
            's3', **settings.aws.dns
        )
        self.vk_client = await self._exit_stack.enter_async_context(
            vk_session
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

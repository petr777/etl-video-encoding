import asyncio
from database import metadata
from sqlalchemy.ext.asyncio import create_async_engine
from settings import settings
from services.db_media import MediaServiceDB


async def async_main():

    engine = create_async_engine(
        settings.pg.dns,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_main())

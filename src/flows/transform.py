import os
import asyncio
import aiofiles
from aiovk import AioVK

from settings import settings
from prefect import task, get_run_logger
from services.ff_media import MediaServicesFF



@task(retries=3, retry_delay_seconds=60)
async def convert(file, size):
    media_services_ff = MediaServicesFF(file)
    await media_services_ff.convert(size=size)

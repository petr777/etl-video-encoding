import os
import asyncio
import aiofiles
from aiovk import AioVK
from database import session_scope
from settings import settings
from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from services.db_media import MediaServiceDB
from services.ff_media import MediaServicesFF
from get_new_files import get_new_files
from extract import download_files
from transform import convert
from load import upload_files

@flow(task_runner=SequentialTaskRunner(), name="video_encoding")
async def video_encoding(size: str):
    new_files = await get_new_files()

    if new_files:
        local_files = await download_files(new_files)

        convert_files = []
        for file in local_files:
            convert_file = await convert(file, size)
            convert_files.append(convert_file)

        ok_files = await upload_files(convert_files)

        print(ok_files)


    # print(new_files)

    # if new_files:
    #     local_files = await download_files(new_files)
    #     for file in local_files:
    #         media_services_ff = MediaServicesFF(file)
    #         async with session_scope() as session:
    #             media_service = MediaServiceDB(session)
    #             await media_service.create(media_services_ff.short_info)
    #         media_services_ff.convert(size='640x360')
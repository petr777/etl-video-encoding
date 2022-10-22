import os
import asyncio
from aiovk import AioVK
from settings import settings
from prefect import flow, task, get_run_logger


async def unload(con_file, s3):
    local_file = settings.temporary_dir / os.path.basename(con_file)
    response = await s3.vk_client.upload_file(local_file, Bucket=settings.aws.bucket_hot,  Key=f'{con_file}')
    return local_file


async def bound_unload(semaphore, new_file, s3):
    async with semaphore:
        return await unload(new_file, s3)


@task(retries=3, retry_delay_seconds=60)
async def upload_files(con_file, backup_dir):

    semaphore = asyncio.Semaphore(10)

    async with AioVK() as s3:
        task = asyncio.ensure_future(bound_unload(semaphore, con_file, s3))
        responses = asyncio.gather(*task)
        return await responses
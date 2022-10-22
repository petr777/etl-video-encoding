import os
import asyncio
import aiofiles
from aiovk import AioVK

from settings import settings
from prefect import task, get_run_logger


async def download(new_file, s3):

    local_file = settings.temporary_dir / os.path.basename(new_file)
    response = await s3.vk_client.get_object(Bucket=settings.aws.bucket_ice, Key=new_file)

    async with response['Body'] as body:
        data = await body.read()
        async with aiofiles.open(local_file, "wb") as out:
            await out.write(data)
        return local_file


async def bound_download(semaphore, new_file, s3):
    async with semaphore:
        return await download(new_file, s3)


@task(retries=3, retry_delay_seconds=60)
async def download_files(new_files):
    logger = get_run_logger()
    semaphore = asyncio.Semaphore(10)
    tasks = []
    async with AioVK() as s3:
        for new_file in new_files:
            task = asyncio.ensure_future(bound_download(semaphore, new_file, s3))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        results = [res for res in await responses]
        logger.info(f'{len(new_file)} media downloaded in temporary_dir')
        return results


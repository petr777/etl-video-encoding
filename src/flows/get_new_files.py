from aiovk import AioVK
from database import session_scope
from settings import settings
from prefect import task, get_run_logger
from services.db_media import MediaServiceDB


async def file_in_vk_gen():
    async with AioVK() as s3:
        paginator = s3.vk_client.get_paginator('list_objects')
        async for result in paginator.paginate(Bucket=settings.aws.bucket_ice):
            for content in result.get('Contents', []):
                if content.get('Size') > 0:
                    yield content.get('Key')


async def vk_files():
    all_file = []
    async for file in file_in_vk_gen():
        all_file.append(file)
    return all_file


async def db_files(vk_files):
    async with session_scope() as session:
        media_service = MediaServiceDB(session)
        return await media_service.get_by_files(vk_files)


@task(retries=3, retry_delay_seconds=60)
async def get_new_files():
    logger = get_run_logger()
    vk_files_list = await vk_files()
    db_files_list = await db_files(vk_files_list)
    new_file = list(set(vk_files_list) - set(db_files_list))
    logger.info(f'{len(new_file)} media added in bucket {settings.aws.bucket_ice}')
    return new_file
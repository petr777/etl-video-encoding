from sqlalchemy.future import select
from models import MoviesInfoModel
from schemas import MediaInfoSchema
import sqlalchemy as sa


class ObjectDoesNotExistError(Exception):
    """Raise it if object does not exist in database."""


class ObjectAlreadyExistError(Exception):
    """Raise it if object already exist in database."""


class MediaServiceDB:

    models = MoviesInfoModel

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_by_files(self, filenames):
        q = select(self.models).filter(MoviesInfoModel.filename.in_(filenames))
        result = await self.db_session.execute(q)
        data = [row.filename for row in result.scalars().all()]
        return data

    async def create(self, info: MediaInfoSchema):
        movie = MoviesInfoModel(**info.dict())
        self.db_session.add(movie)
        try:
            await self.db_session.commit()
        except sa.exc.IntegrityError:
            raise ObjectAlreadyExistError
        await self.db_session.refresh(movie)
        return movie





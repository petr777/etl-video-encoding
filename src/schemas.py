from pydantic import BaseModel


class MediaInfoSchema(BaseModel):
    filename: str
    width: int
    height: int
    duration: float
    format: str
    acodec: str
    vcodec: str

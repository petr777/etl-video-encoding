from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import declarative_mixin
from database import Base


@declarative_mixin
class TimestampMixin:

    created_at = sa.Column(
        sa.DateTime(timezone=False), default=lambda: datetime.utcnow()
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=False),
        default=lambda: datetime.utcnow(),
        onupdate=datetime.utcnow,
    )


class MoviesInfoModel(Base, TimestampMixin):

    __tablename__ = "movies_info"

    filename = sa.Column(sa.String(length=128), nullable=False, unique=True, primary_key=True)

    width = sa.Column(
        sa.Integer, sa.CheckConstraint("width>0"), nullable=False
    )
    height = sa.Column(
        sa.Integer, sa.CheckConstraint("width>0"), nullable=False
    )
    duration = sa.Column(
        sa.Numeric(14, 7), sa.CheckConstraint("duration>0"), nullable=False
    )
    format = sa.Column(sa.String(length=64), nullable=True, unique=False)
    acodec = sa.Column(sa.String(length=64), nullable=True, unique=False)
    vcodec = sa.Column(sa.String(length=64), nullable=True, unique=False)


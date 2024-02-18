import datetime

from sqlalchemy import String, Float, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, INTEGER, DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk


class DeviceData(Base):
    __tablename__ = 'device_data'

    id: Mapped[intpk]
    user_id: Mapped[int] = ForeignKey(mapped_column(ForeignKey("user.id")))
    device_id: Mapped[int] = mapped_column()
    x: Mapped[float] = mapped_column()
    y: Mapped[float] = mapped_column()
    z: Mapped[float] = mapped_column()
    create_time: Mapped[datetime.datetime] = mapped_column(unique=True, nullable=False)

import datetime

from pydantic import BaseModel


class DeviceDataIn(BaseModel):
    device_id: int
    x: float
    y: float
    z: float


class DeviceDataOut(BaseModel):
    device_id: int
    x: float
    y: float
    z: float
    create_time: datetime.time


class MinValues(BaseModel):
    x: float
    y: float
    z: float


class MaxValues(BaseModel):
    x: float
    y: float
    z: float


class SummaValues(BaseModel):
    x: float
    y: float
    z: float


class MedianValues(BaseModel):
    x: float
    y: float
    z: float

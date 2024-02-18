import datetime
from typing import Any, Sequence

from sqlalchemy import delete, select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.device_data import DeviceData


class DeviceDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_device_data(self, device_data) -> DeviceData:
        _deviceData = DeviceData(**device_data)
        self.session.add(_deviceData)
        await self.session.commit()
        await self.session.refresh(_deviceData)
        return _deviceData

    async def get_by_id(self, device_data_id: int) -> DeviceData | None:
        statement = select(DeviceData).where(DeviceData.id == device_data_id)
        return await self.session.scalar(statement=statement)

    async def get_by_device_id(self, device_data_id: int) -> list[DeviceData]:
        statement = select(DeviceData).where(DeviceData.device_id == device_data_id).order_by(DeviceData.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_devices_by_user_id(self, device_data_user_id: int) -> list[DeviceData]:
        statement = select(DeviceData).where(DeviceData.user_id == device_data_user_id).order_by(
            DeviceData.id).distinct(DeviceData.device_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_by_user_id(self, device_data_user_id: int) -> list[DeviceData]:
        statement = select(DeviceData).where(DeviceData.user_id == device_data_user_id).order_by(DeviceData.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_by_user_id_before_create_time(self, device_data_user_id: int, time_before: datetime.time) -> list[
        DeviceData]:
        statement = select(DeviceData).where(
            DeviceData.user_id == device_data_user_id and DeviceData.create_time <= time_before).order_by(DeviceData.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_by_device_id_interval_create_time(self, device_data_user_id: int, time_from: datetime.datetime,
                                                    time_to: datetime.datetime) -> list[DeviceData]:
        statement = select(DeviceData).where(
            DeviceData.user_id == device_data_user_id and DeviceData.create_time <= time_from and DeviceData.create_time >= time_to).order_by(
            DeviceData.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_all(self) -> list[DeviceData]:
        statement = select(DeviceData).order_by(DeviceData.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(DeviceData))
        await self.session.commit()

    async def delete_by_id(self, device_data_id: int) -> DeviceData | None:
        _deviceData = await self.get_by_id(device_data_id=device_data_id)
        statement = delete(DeviceData).where(DeviceData.id == device_data_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _deviceData

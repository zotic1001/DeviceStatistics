import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import user, device_data
from app.db import get_session
from app.models.user import User as UserModel
from app.models.device_data import DeviceData as DeviceDataModel
from app.schemas.device_data import DeviceDataIn, DeviceDataOut, MinValues, MaxValues, MedianValues, SummaValues
from app.schemas.token import Token, TokenData
from app.schemas.user import ChangePasswordIn, UserIn, UserOut
from app.services.utils import UtilsService, oauth2_scheme
from app.settings import settings


class DeviceDataService:
    @staticmethod
    async def post_device_data(session: AsyncSession, current_user: UserModel, device_data_in: DeviceDataIn):
        new_device_data = await device_data.DeviceDao(session).create(
            DeviceDataModel(
                user_id=current_user.id,
                device_id=device_data_in.device_id,
                x=device_data_in.x,
                y=device_data_in.y,
                z=device_data_in.z,
                create_time=datetime.datetime.utcnow()
            )
        )
        logger.info(f"New device data posted successfully: {new_device_data}!!!")
        return JSONResponse(
            content={"message": "New device data posted successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def get_current_user_device_data(session: AsyncSession, current_user: UserModel):
        user_device_data = await device_data.DeviceDao(session).get_by_user_id(current_user.id)
        return [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]

    @staticmethod
    async def get_current_user_device_data_between_time(session: AsyncSession, current_user: UserModel,
                                                        time_from: datetime.datetime, time_to: datetime.datetime):
        if time_from < time_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time from can't be less time to",
            )
        user_device_data = await device_data.DeviceDao(session).get_by_device_id_interval_create_time(current_user.id,
                                                                                                      time_from,
                                                                                                      time_to)
        return [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]

    @staticmethod
    async def get_current_user_device_data_min_values(session: AsyncSession, current_user: UserModel) -> MinValues:
        user_device_data = await device_data.DeviceDao(session).get_by_user_id(current_user.id)

        min_x = min(map(lambda _device_data: _device_data.x,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        min_y = min(map(lambda _device_data: _device_data.y,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        min_z = min(map(lambda _device_data: _device_data.z,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        return MinValues(x=min_x, y=min_y, z=min_z)

    @staticmethod
    async def get_current_user_device_data_max_values(session: AsyncSession, current_user: UserModel) -> MaxValues:
        user_device_data = await device_data.DeviceDao(session).get_by_user_id(current_user.id)

        max_x = max(map(lambda _device_data: _device_data.x,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        max_y = max(map(lambda _device_data: _device_data.y,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        max_z = max(map(lambda _device_data: _device_data.z,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        return MaxValues(x=max_x, y=max_y, z=max_z)

    @staticmethod
    async def get_current_user_device_data_device_counts(session: AsyncSession, current_user: UserModel):
        user_devices = await device_data.DeviceDao(session).get_devices_by_user_id(current_user.id)
        return len(user_devices)

    @staticmethod
    async def get_current_user_device_data_sum_values(session: AsyncSession, current_user: UserModel) -> SummaValues:
        user_device_data = await device_data.DeviceDao(session).get_by_user_id(current_user.id)

        sum_x = sum(map(lambda _device_data: _device_data.x,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        sum_y = sum(map(lambda _device_data: _device_data.y,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        sum_z = sum(map(lambda _device_data: _device_data.z,
                        [DeviceDataOut.model_validate(_device_data) for _device_data in user_device_data]))
        return SummaValues(x=sum_x, y=sum_y, z=sum_z)

    @staticmethod
    async def get_current_user_device_data_median_values(session: AsyncSession,
                                                         current_user: UserModel) -> MedianValues:
        user_device_data = await device_data.DeviceDao(session).get_by_user_id(current_user.id)

        def calculate_median(values: List[float]):
            return values.sort()[len(values) // 2 + 1]

        median_x = calculate_median(list(map(lambda _device_data: _device_data.x,
                                             [DeviceDataOut.model_validate(_device_data) for _device_data in
                                              user_device_data])))
        median_y = calculate_median(list(map(lambda _device_data: _device_data.y,
                                             [DeviceDataOut.model_validate(_device_data) for _device_data in
                                              user_device_data])))
        median_z = calculate_median(list(map(lambda _device_data: _device_data.z,
                                             [DeviceDataOut.model_validate(_device_data) for _device_data in
                                              user_device_data])))

        return MedianValues(x=median_x, y=median_y, z=median_z)

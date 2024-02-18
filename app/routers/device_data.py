import datetime

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.device_data import DeviceDataIn, DeviceDataOut, MinValues, MaxValues, SummaValues, MedianValues
from app.schemas.token import Token
from app.schemas.user import ChangePasswordIn, UserIn, UserOut
from app.services.device_data import DeviceDataService
from app.services.user import UserService

router = APIRouter(tags=["DeviceData"], prefix="/device_data")


@router.post("/device_data", status_code=status.HTTP_201_CREATED)
async def create_device_data(device_data: DeviceDataIn,
                             current_user=Depends(UserService.get_current_user),
                             session: AsyncSession = Depends(get_session),
                             ):
    return await DeviceDataService.post_device_data(current_user=current_user, device_data_in=device_data,
                                                    session=session)


@router.get("/get_user_device_data", status_code=status.HTTP_200_OK)
async def get_user_device_data(current_user=Depends(UserService.get_current_user),
                               session: AsyncSession = Depends(get_session)) -> list[DeviceDataOut]:
    return await DeviceDataService.get_current_user_device_data(current_user=current_user, session=session)


@router.get("/get_user_devices_min_values/", status_code=status.HTTP_200_OK)
async def get_user_devices_min_values(
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> MinValues:
    return await DeviceDataService.get_current_user_device_data_min_values(current_user=current_user, session=session)


@router.get("/get_user_devices_max_values/", status_code=status.HTTP_200_OK)
async def get_user_devices_max_values(
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> MaxValues:
    return await DeviceDataService.get_current_user_device_data_max_values(current_user=current_user, session=session)


@router.get("/get_user_devices_sum_values/", status_code=status.HTTP_200_OK)
async def get_user_devices_sum_values(
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> SummaValues:
    return await DeviceDataService.get_current_user_device_data_sum_values(current_user=current_user, session=session)


@router.get("/get_user_devices_median_values/", status_code=status.HTTP_200_OK)
async def get_user_devices_median_values(
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> MedianValues:
    return await DeviceDataService.get_current_user_device_data_median_values(current_user=current_user,
                                                                              session=session)


@router.get("/get_user_devices_count/", status_code=status.HTTP_200_OK)
async def get_user_devices_count(
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> int:
    return await DeviceDataService.get_current_user_device_data_device_counts(current_user=current_user,
                                                                              session=session)


@router.get("/get_user_devices_data_between/", status_code=status.HTTP_200_OK)
async def get_user_devices_median_values(
        time_from: datetime.datetime,
        time_to: datetime.datetime = datetime.datetime.now(),
        current_user=Depends(UserService.get_current_user),
        session: AsyncSession = Depends(get_session),
) -> int:
    return await DeviceDataService.get_current_user_device_data_between_time(time_from=time_from,
                                                                             time_to=time_to,
                                                                             current_user=current_user,
                                                                             session=session)

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Path

from app.schemas.user import UserUpdate, UserCreate, UserUpdatePass
from app.settings import api_settings
from .deps import UserServiceDep
from app.deps import CurrentActiveUserDep
from app.common.schemas import UserDTO, MessageDTO

router = APIRouter(
    prefix=api_settings.USERS_PREFIX,
)


@router.get('/get_user/{userSid}', response_model=UserDTO)
async def get_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_sid: Annotated[UUID, Path(..., alias="userSid")]
) -> UserDTO:
    """
    Get user by id
    """
    return await service.get_user(user_sid=user_sid, current_user=current_user)


@router.get('/get_users', response_model=list[UserDTO])
async def get_users(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep
) -> list[UserDTO]:
    """
    Get users
    """
    return await service.get_users(current_user=current_user)


@router.get('/get_me', response_model=UserDTO)
async def get_me(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep
) -> UserDTO:
    return await service.get_me(current_user=current_user)


@router.post(
    '/create_user',
    response_model=UserDTO
)
async def create_user(
    service: UserServiceDep,
    user_data: UserCreate,
) -> UserDTO:
    return await service.create_user(
        data=user_data
    )


@router.put('/update_me', response_model=MessageDTO)
async def update_me(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    data: Annotated[UserUpdate, Body(...)],
) -> MessageDTO:

    await service.update_me(current_user=current_user, data=data)

    return MessageDTO(message="Пользователь обновлен")


@router.put('/change_password', response_model=MessageDTO)
async def update_password(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    data: Annotated[UserUpdatePass, Body(...)],
) -> MessageDTO:

    await service.update_password(current_user=current_user, data=data)

    return MessageDTO(message="Пользователь обновлен")


@router.post('/block_me', response_model=MessageDTO)
async def block_me(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
) -> MessageDTO:

    await service.block_me(current_user=current_user)

    return MessageDTO(message="Учетная запись отключена")


@router.post('/block_user/{userSid}', response_model=MessageDTO)
async def block_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_sid: Annotated[UUID, Path(..., alias="userSid")]
) -> MessageDTO:

    await service.block_user(current_user=current_user, user_sid=user_sid)

    return MessageDTO(message="Учетная запись пользователя отключена")


@router.post('/unlock_user/{userSid}', response_model=MessageDTO)
async def unlock_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_sid: Annotated[UUID, Path(..., alias="userSid")]
) -> MessageDTO:

    await service.unlock_user(current_user=current_user, user_sid=user_sid)

    return MessageDTO(message="Учетная запись пользователя активирована")



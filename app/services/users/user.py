import logging
from uuid import uuid4, UUID

from fastapi import HTTPException

from app.deps import CurrentActiveUserDep, check_user_admin
from app.utils import DateTimeManager
from app.common.adapters import PostgresStorageAdapter
from app.common.schemas import UserDTO, MessageDTO
from app.core.auth import password_manager
from app.schemas.user import UserCreate, UserUpdate, UserUpdatePass


class UserService:
    def __init__(
        self,
        *,
        logger: logging.Logger,
        postgres_adapter: PostgresStorageAdapter,
    ) -> None:
        self._logger = logger
        self._postgres_adapter = postgres_adapter

    async def commit_user(self) -> None:
        await self._postgres_adapter.commit_user()

    @staticmethod
    def _get_user_model(
        *,
        user_model: UserDTO | None = None,
        user_data: UserCreate,
    ) -> UserDTO:
        hashed_password = password_manager.get_hashed_password(
            password=user_data.hashed_password,
        )
        created_at = DateTimeManager.get_now_utc()
        fullname = ' '.join(filter(None, [user_data.first_name, user_data.last_name, user_data.middle_name]))
        if user_model:
            return UserDTO(
                sid=user_model.sid,
                email=user_model.email,
                fullname=user_model.fullname,
                role=user_model.role,
                hashed_password=user_model.hashed_password,
                created_at=created_at,
                updated_at=created_at,
            )

        return UserDTO(
            sid=uuid4(),
            email=user_data.email,
            fullname=fullname,
            hashed_password=hashed_password,
            created_at=created_at,
            updated_at=created_at
        )

    @staticmethod
    def _get_user_updated_model(
        *,
        user_model: UserDTO,
        updated_data: UserUpdate,
    ) -> UserDTO:
        fullname = ' '.join(filter(None, [
            updated_data.first_name,
            updated_data.last_name,
            updated_data.middle_name
        ]))
        user_updated_model = user_model.model_copy()
        updated_at = DateTimeManager.get_now_utc()
        user_updated_model.updated_at = updated_at
        user_updated_model.fullname = fullname
        return user_updated_model

    @staticmethod
    async def get_me(
        *,
        current_user: CurrentActiveUserDep
    ) -> UserDTO:
        return UserDTO.model_validate(current_user)

    async def get_user(
        self,
        *,
        current_user: CurrentActiveUserDep,
        user_sid: UUID,
    ) -> UserDTO | None:
        await check_user_admin(current_user=current_user)
        user = await self._postgres_adapter.get_user(user_sid=user_sid)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User does not exist",
            )
        return UserDTO.model_validate(user)


    async def get_users(
        self,
        *,
        current_user: CurrentActiveUserDep,
    ) -> list[UserDTO]:
        await check_user_admin(current_user=current_user)
        users = await self._postgres_adapter.get_users()
        return users

    async def create_user(
        self,
        *,
        data: UserCreate,
    ) -> UserDTO:
         user_by_email = await self._postgres_adapter.get_user_by_email(
             user_email=data.email,
         )
         if user_by_email:
             raise ValueError("Пользователь с такой почтой уже существует")

         if data.hashed_password != data.confirm_hashed_password:
             raise ValueError("Пароли не совпадают")

         user_model = self._get_user_model(
             user_model=user_by_email, user_data=data
         )
         await self._postgres_adapter.create_user(user_model=user_model)
         await self.commit_user()
         return user_model

    async def update_me(
        self,
        *,
        current_user: CurrentActiveUserDep,
        data: UserUpdate,
    ) -> UserDTO:
        user_updated_model = self._get_user_updated_model(
            user_model=current_user,
            updated_data=data
        )
        await self._postgres_adapter.update_user(user_model=user_updated_model)
        await self.commit_user()
        return UserDTO.model_validate(
            obj=user_updated_model, from_attributes=True
        )

    async def update_password(
        self,
        *,
        current_user: CurrentActiveUserDep,
        data: UserUpdatePass,
    ) -> MessageDTO:
        user = await self._postgres_adapter.get_user(
            user_sid=current_user.sid
        )
        if data.hashed_password != data.confirm_hashed_password:
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match",
            )

        hashed_password = password_manager.get_hashed_password(
            password=data.hashed_password,
        )
        await self._postgres_adapter.update_user_password(
            user_sid=user.sid,
            new_hashed_password=hashed_password,
        )
        await self.commit_user()
        return MessageDTO(message="Пользователь обновлен")

    async def block_me(
        self,
        *,
        current_user: CurrentActiveUserDep,
    ) -> MessageDTO:
        await self._postgres_adapter.block_user(user_sid=current_user.sid)
        await self._postgres_adapter.commit_user()
        return MessageDTO(message="Учетная запись успешно отключена")

    async def block_user(
        self,
        current_user: CurrentActiveUserDep,
        user_sid: UUID
    ) -> MessageDTO:
        await check_user_admin(current_user=current_user)
        user = await self._postgres_adapter.get_user(user_sid=user_sid)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User does not exist",
            )
        await self._postgres_adapter.block_user(user_sid=user_sid)
        await self._postgres_adapter.commit_user()
        return MessageDTO(message="Учетная запись успешно отключена")

    async def unlock_user(
        self,
        *,
        current_user: CurrentActiveUserDep,
        user_sid: UUID
    ) -> MessageDTO:
        await check_user_admin(current_user=current_user)
        user = await self._postgres_adapter.get_user(user_sid=user_sid)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User does not exist",
            )
        await self._postgres_adapter.unlock_user(user_sid=user_sid)
        await self._postgres_adapter.commit_user()
        return MessageDTO(message="Учетная запись успешно отключена")



from fastapi import HTTPException

from .auth import CurrentActiveUserDep
from app.enums import UserRoleEnum


async def check_user_admin(
    current_user: CurrentActiveUserDep
) -> None:
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
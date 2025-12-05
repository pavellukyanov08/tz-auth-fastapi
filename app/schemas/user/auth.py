from pydantic import Field

from app.common.schemas import CamelDTO, EmailDTO


class AuthLogin(CamelDTO, EmailDTO):
    password: str = Field(
        ...,
        max_length=256,
        description="User password",
    )

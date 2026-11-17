from pydantic import BaseModel, Field, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, pw: str) -> str:
        if len(pw.encode("utf-8")) > 72:
            raise ValueError("password must be at most 72 bytes")
        return pw


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    model_config = {"from_attributes": True}
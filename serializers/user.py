from pydantic import BaseModel, field_validator, ConfigDict


class UserRequestSerializer(BaseModel):
    email: str
    name: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(value) > 128:
            raise ValueError("Password must be at max 128 characters long")
        if value.isnumeric():
            raise ValueError("Password cannot be only numbers")
        return value


class UserResponseSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

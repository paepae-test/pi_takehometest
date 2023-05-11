from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass

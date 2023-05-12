from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class Auth(BaseModel):
    username: str
    password: str

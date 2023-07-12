from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    user_name: str
    password: str


class Token(BaseModel):
    token: str
    account: str
    phone: str
    name: str


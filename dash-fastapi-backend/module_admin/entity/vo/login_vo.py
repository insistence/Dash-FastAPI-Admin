from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    user_name: str
    password: str
    captcha: str
    session_id: Optional[str]


class Token(BaseModel):
    token: str
    account: str
    phone: str
    name: str


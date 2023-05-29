from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    user_name: str
    password: str
    user_request: Optional[str] = None


class Token(BaseModel):
    token: str
    account: str
    phone: str
    name: str


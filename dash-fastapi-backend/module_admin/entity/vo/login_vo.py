from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    user_name: str
    password: str
    captcha: Optional[str]
    session_id: Optional[str]
    login_info: Optional[dict]


class Token(BaseModel):
    access_token: str
    token_type: str

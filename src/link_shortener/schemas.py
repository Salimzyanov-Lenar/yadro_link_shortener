from pydantic import BaseModel, HttpUrl, conint
from datetime import datetime


class LinkCreate(BaseModel):
    original_url: HttpUrl
    expire_in_days: conint(ge=1, le=3) = 1


class LinkOut(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime
    expire_at: datetime
    is_active: bool
    redirect_count: int

    class Config:
        orm_mode = True

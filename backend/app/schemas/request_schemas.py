from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator


class ChannelCreate(BaseModel):
    channel_url: Optional[str] = Field(None, alias="url")
    channel_id: Optional[str] = Field(None, alias="id")

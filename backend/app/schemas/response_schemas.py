from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator


class Channel(BaseModel):
    channel_id: str = Field(..., alias="id")
    channel_name: str = Field(..., alias="name")
    channel_description: str = Field(..., alias="description")
    channel_type: str = Field(..., alias="type")
    channel_subscribers: int = Field(..., alias="subscribers")


class ChannelList(BaseModel):
    count = int
    channels = List[Channel]


class ChannelInfo(BaseModel):
    ...


class ChannelAllPosts(BaseModel):
    ...


class ChannelPostInfo(BaseModel):
    ...


class ChannelPostViews(BaseModel):
    ...


class ChannelPostReposts(BaseModel):
    ...


class ChannelPostReactions(BaseModel):
    ...


class ChannelPostComments(BaseModel):
    ...


class ChannelPostContent(BaseModel):
    ...


class ChannelPostSummary(BaseModel):
    ...


class ChannelsComparing(BaseModel):
    ...


class Dashboard(BaseModel):
    ...


class Predictions(BaseModel):
    ...

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator


class DefaultError(BaseModel):
    detail: str
    error: str


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


class ChannelPost(BaseModel):
    post_id: str = Field(..., alias="id")
    post_text: str = Field(..., alias="text")
    post_timestamp: str = Field(..., alias="timestamp")


class ChannelAllPosts(BaseModel):
    count: int
    posts: List[ChannelPost]


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

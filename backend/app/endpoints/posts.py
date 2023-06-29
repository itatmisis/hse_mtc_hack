from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@router.get(
    '/{channel_id}/posts',
    response_model=response_schemas.ChannelAllPosts,
)
async def get_all_posts(channel_id: int, db: Session = Depends(get_db)):
    """
    Get all posts in a channel
    """
    posts = crud.get_posts_by_channel_id(db, channel_id)
    return posts


@router.get(
    '/{channel_id}/posts/{post_id}',
    response_model=response_schemas.ChannelPost,
)
async def get_post(channel_id: int, post_id: int, db: Session = Depends(get_db)):
    """
    Get a post in a channel
    """
    post = crud.get_post_by_id(db, channel_id, post_id)
    if not post:

        log.error(f"Post {post_id} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found",
        )
    return post

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.utils import tg

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@router.get(
    "/{group_handle}/posts",
    response_model=response_schemas.ChannelAllPosts,
)
async def get_all_posts(group_handle: str, db: Session = Depends(get_db)):
    """
    Get all posts in a channel
    """
    try:
        handle = (
            group_handle.split("/")[-1]
            if group_handle.startswith("http") or "t.me" in group_handle.split("/")[-2]
            else group_handle
        )
    except IndexError:
        handle = group_handle

    if not crud.get_channel_id_by_handle(db, handle):
        r = tg.parse_channel(handle)

        if not r:
            log.error(f"Channel {handle} not found")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Channel {handle} not found",
            )

    try:
        posts = crud.get_posts_by_channel_id(db, handle)
    except Exception as e:
        db.rollback()
        log.error(f"Error getting posts for channel {handle}: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting posts for channel {handle}: {e}",
        )
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="try again later",
        )
    return posts


@router.get(
    "/{group_handle}/posts/{post_id}",
    response_model=response_schemas.ChannelPost,
)
async def get_post(group_handle: str, post_id: str, db: Session = Depends(get_db)):
    """
    Get a post in a channel
    """
    post = crud.get_post_by_id(db, group_handle, post_id)
    if not post:
        log.error(f"Post {post_id} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found",
        )
    return post


@router.get("/{group_handle}/posts/top", response_model=response_schemas.ChannelTopPosts)
async def get_top_posts(group_handle: str, db: Session = Depends(get_db)):
    post = crud.get_top_posts_by_channel_handle(db, group_handle)
    if not post:
        log.error(f"Posts from {group_handle} not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {group_handle} not found",
        )
    return post

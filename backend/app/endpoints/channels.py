from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import settings
from app.config import log
from app.core import schemas
from app.core.dependencies import get_db
from app.core import crud

router = APIRouter(
    prefix="/channels",
    tags=["channeld"],
)


@router.get("/", response_model=schemas.ChannelList)
async def get_channels(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all channels
    """
    channels = crud.get_channels(db, skip=skip, limit=limit)
    return {"count": len(channels), "channels": channels}


@router.post("/")
async def add_channel(
    channel: schemas.Channel,
    db: Session = Depends(get_db),
):
    """
    Add a channel
    """
    channel = crud.add_channel(db, channel)
    return channel


@router.get("/{channel_id}", response_model=schemas.Channel)
async def get_channel(
    channel_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a channel
    """
    channel = crud.get_channel(db, channel_id)
    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel {channel_id} not found",
        )
    return channel


@router.delete("/{channel_id}")
async def delete_channel(
    channel_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a channel
    """
    channel = crud.delete_channel(db, channel_id)
    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel {channel_id} not found",
        )
    return channel

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


@router.post(
    "/compare",
    response_model=response_schemas.ChannelsComparing,
)
async def compare_channels(
    comparing: request_schemas.ChannelsComparing, db: Session = Depends(get_db)
):
    """
    Compare multiple channels based on the selected metrics.
    """
    pass

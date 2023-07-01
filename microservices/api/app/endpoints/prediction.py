from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud

router = APIRouter(
    prefix="/predictions",
    tags=["channels"],
)


@router.get(
    '/{channel_id}',
    response_model=response_schemas.ChannelPrediction,
)
async def get_prediction(channel_id: int, db: Session = Depends(get_db)):
    """
    Get a prediction in a channel
    """
    pass

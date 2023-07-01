from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    '/'
)
async def get_prediction():
    """
    Get a prediction in a channel
    """
    return {'success': True}

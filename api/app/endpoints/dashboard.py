from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get(
    '/',
    response_model=response_schemas.Dashboard,
)
async def get_prediction(db: Session = Depends(get_db)):
    """
    Get a prediction in a channel
    """
    pass

from os import walk
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.endpoints.channels import router

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@router.get(
    '/{channel_id}/metrics',
    response_model=response_schemas.ChannelMetrics,
)
async def get_all_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get all metrics for a channel
    """
    metrics = crud.get_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/reposts',
    response_model=response_schemas.ChannelRepostsMetrics,
)
async def get_reposts_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get reposts metrics for a channel
    """
    metrics = crud.get_reposts_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/views',
    response_model=response_schemas.ChannelViewsMetrics,
)
async def get_views_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get views metrics for a channel
    """
    metrics = crud.get_views_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/comments',
    response_model=response_schemas.ChannelCommentsMetrics,
)
async def get_comments_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get comments metrics for a channel
    """
    metrics = crud.get_comments_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/sentiment',
    response_model=response_schemas.ChannelSentimentMetrics,
)
async def get_sentiment_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get sentiment metrics for a channel
    """
    metrics = crud.get_sentiment_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/reactions',
    response_model=response_schemas.ChannelReactionsMetrics,
)
async def get_reactions_metrics(
        channel_id: int,
        type: Optional[str] = None,
        db: Session = Depends(get_db)
    ):
    """
    Get reactions metrics for a channel
    """
    if type is None:
        metrics = crud.get_reactions_metrics_by_channel_id(db, channel_id)
    elif type == 'positive':
        metrics = crud.get_positive_reactions_metrics_by_channel_id(db, channel_id)
    elif type == 'negative':
        metrics = crud.get_negative_reactions_metrics_by_channel_id(db, channel_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid reaction type {type}",
        )

    return metrics


@router.get(
    '/{channel_id}/metrics/content',
    response_model=response_schemas.ChannelContentMetrics,
)
async def get_content_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get content metrics for a channel
    """
    metrics = crud.get_content_metrics_by_channel_id(db, channel_id)
    return metrics


@router.get(
    '/{channel_id}/metrics/summary',
    response_model=response_schemas.ChannelSummaryMetrics,
)
async def get_summary_metrics(channel_id: int, db: Session = Depends(get_db)):
    """
    Get summary metrics for a channel
    """
    metrics = crud.get_summary_metrics_by_channel_id(db, channel_id)
    return metrics

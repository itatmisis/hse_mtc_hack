from sqlalchemy.orm import Session

from app.models import db_models
from app.schemas import response_schemas
from app.config import log


def get_posts_by_channel_id(
    db: Session,
    channel_id: str
) -> response_schemas.ChannelAllPosts | None:
    """
    Get all posts in a channel
    """
    posts = db.query(
        db_models.Post.id.label("post_id"),
        db_models.Post.date.label("post_date"),
        db_models.PostMetrics.views.label("views"),
        db_models.PostMetrics.comments.label("comments"),
    ).join(db_models.PostMetrics).filter(
        db_models.Post.channel_id == channel_id
    ).all()

    if not posts:
        log.error(f"Posts not found in channel {channel_id}")
        return None

    return response_schemas.ChannelAllPosts(
        count=len(posts),
        posts=[response_schemas.ChannelPost.from_orm(post) for post in posts],
    )

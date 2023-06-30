from sqlalchemy.orm import Session

from app.models import db_models
from app.schemas import response_schemas
from app.config import log


def get_posts_by_channel_id(
    db: Session,
    handle: str
) -> response_schemas.ChannelAllPosts | None:
    """
    Get all posts in a channel
    """

    channel_id = get_channel_id_by_handle(db, handle)

    posts = db.query(
        db_models.Post.post_id.label("post_id"),
        db_models.Post.post_date.label("post_date"),
        db_models.PostMetrics.views.label("views"),
        db_models.PostMetrics.comments.label("comments"),
    ).join(db_models.PostMetrics).filter(
        db_models.Post.channel_id == channel_id
    ).all()

    if len(posts) == 0:
        log.error(f"Posts not found in channel {channel_id}")
        return None

    log.info(f'{posts}')

    return response_schemas.ChannelAllPosts(
        count=len(posts),
        posts=[response_schemas.ChannelPost.from_orm(post) for post in posts],
    )


def get_post_by_id(
    db: Session,
    channel_id: str,
    post_id: str
) -> response_schemas.ChannelPost | None:
    """
    Get a post by its id
    """
    post = db.query(
        db_models.Post.post_id.label("post_id"),
        db_models.Post.post_date.label("post_date"),
        db_models.PostMetrics.views.label("views"),
        db_models.PostMetrics.comments.label("comments"),
    ).join(db_models.PostMetrics).filter(
        db_models.Post.post_id == post_id,
        db_models.Post.channel_id == channel_id
    ).first()

    db_reactions = db.query(
        db_models.Reaction.reaction_desc,
        db_models.Reaction.count,
    ).filter(
        db_models.Reaction.post_id == post_id
    ).all()

    if db_reactions:
        reactions = {
            reaction.reaction_desc: reaction.count
            for reaction in db_reactions
        }
    else:
        reactions = None

    if not post:
        log.error(f"Post {post_id} not found")
        return None

    return response_schemas.ChannelPost(
        reactions=reactions,
        **post.__dict__
    )


def get_channel_id_by_handle(
    db: Session,
    channel_id: str
) -> bool:

    return db.query(
        db_models.Channel.channel_id
    ).filter(
        db_models.Channel.channel_handle == channel_id
    ).first()


def get_top_posts_by_channel_handle(
    db: Session,
    channel_handle: str
) -> response_schemas.ChannelTopPosts | None:
    """
    Get top posts in a channel
    """

    channel_id = get_channel_id_by_handle(db, channel_handle)

    posts = db.query(
        db_models.Post.post_id.label("post_id"),
        db_models.Post.post_date.label("post_date"),
        db_models.PostMetrics.views.label("views"),
        db_models.PostMetrics.comments.label("comments"),
    ).join(db_models.PostMetrics).filter(
        db_models.Post.channel_id == channel_id
    ).order_by(
        db_models.PostMetrics.views.desc()
    ).limit(10).all()

    if not posts:
        log.error(f"Posts not found in channel {channel_id}")
        return None

    return response_schemas.ChannelTopPosts(
        count=len(posts),
        posts=[response_schemas.ChannelPost.from_orm(post) for post in posts],
    )

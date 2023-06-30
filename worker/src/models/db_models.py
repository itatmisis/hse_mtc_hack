from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"
    __table_args__ = (
        Index("idx_channel_name", "channel_name"),
        Index("idx_added_date", "added_date"),
    )

    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String)
    channel_handle = Column(String)
    added_date = Column(DateTime)


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (Index("idx_post_date", "post_date"),)

    post_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    content = Column(String)
    post_date = Column(DateTime)


class PostMetrics(Base):
    __tablename__ = "post_metrics"

    metric_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    views = Column(Integer)
    reposts = Column(Integer)
    comments = Column(Integer)
    links = Column(Integer)
    images = Column(Integer)
    videos = Column(Integer)
    recorded_date = Column(DateTime)


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    content = Column(String)
    comment_date = Column(DateTime)


class Reaction(Base):
    __tablename__ = "reactions"

    reaction_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    reaction_desc = Column(String)
    count = Column(Integer)


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    sentiment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    sentiment_score = Column(Numeric)
    sentiment_label = Column(String)
    recorded_date = Column(DateTime)


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    predicted_effectiveness = Column(Numeric)
    prediction_date = Column(DateTime)


class ComparisonMetrics(Base):
    __tablename__ = "comparison_metrics"

    comparison_id = Column(Integer, primary_key=True)
    channel1_id = Column(Integer, ForeignKey("channels.channel_id"))
    channel2_id = Column(Integer, ForeignKey("channels.channel_id"))
    metric = Column(String)
    comparison_date = Column(DateTime)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_username", "username"),
        Index("idx_created_date", "created_date"),
    )

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    role = Column(String)
    created_date = Column(DateTime)

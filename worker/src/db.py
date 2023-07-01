#!/usr/bin/env python3
# region Dependencies
from datetime import date, datetime, timedelta
from os import getenv
from time import sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import List, Tuple, Union
from sqlalchemy.exc import OperationalError as sqlalchemyOpError
from psycopg2 import OperationalError as psycopg2OpError
# endregion

# region Local imports
from config import log
from models.db_models import Channel, Post, PostMetrics, Comment, Reaction, SentimentAnalysis, Base
# endregion


class DBManager:
    def __init__(self, pg_user, pg_pass, pg_host, pg_port, pg_db):
        self.pg_user = pg_user
        self.pg_pass = pg_pass
        self.pg_host = pg_host
        self.pg_port = pg_port
        self.pg_db = pg_db
        connected = False
        while not connected:
            try:
                self._connect()
            except (sqlalchemyOpError, psycopg2OpError):
                sleep(2)
            else:
                connected = True
        self._update_db()

    def __del__(self):
        """Close the database connection when the object is destroyed"""
        self._close()

    # region Connection setup
    def _connect(self) -> None:
        """Connect to the postgresql database"""
        log.debug(f"Connecting to DB: postgresql+psycopg2://{self.pg_user}:{self.pg_pass}@{self.pg_host}:{self.pg_port}\
/{self.pg_db}")
        self.engine = create_engine(f'postgresql+psycopg2://{self.pg_user}:{self.pg_pass}@{self.pg_host}:{self.pg_port}\
/{self.pg_db}',
                                    pool_pre_ping=True)
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def _close(self) -> None:
        """Closes the database connection"""
        log.warning("Closing DB connection...")
        self.session.close_all()

    # def _recreate_tables(self) -> None:  # Important: Do not use in production!
    #     """Removes and recreates all tables in DB"""
    #     Base.metadata.drop_all(self.engine)
    #     Base.metadata.create_all(self.engine)

    def _update_db(self) -> None:
        """Create the database structure if it doesn't exist (update)"""
        # Create the tables if they don't exist
        Base.metadata.create_all(self.engine)
    # endregion

    def add_channel_records(self, data: dict):
        """Insert channel info, all of its messages, reactions, comments, and comment reactions into the database."""
        try:
            # Check if the channel exists in the database
            log.info(f"Checking if channel \"{data['name']}\" exists in the database...")
            channel = self.session.query(Channel).filter(Channel.channel_id == data['id']).first()
            if not channel:
                # Create a new channel record
                log.debug(f"Adding channel \"{data['name']}\" to the database...")
                log.debug(f"Channel data: {data}")
                channel = Channel(channel_id=data['id'],
                                  channel_name=data['name'],
                                  channel_handle=data['handle'],
                                  added_date=datetime.now())
                self.session.add(channel)
                self.session.commit()
            else:
                # Update the channel name and handle
                channel.channel_name = data['name']
                channel.channel_handle = data['handle']
                log.debug(f"Updating channel \"{data['name']}\" in the database...")
                self.session.commit()
            for pid, post in data['messages'].items():
                # Check if the post exists in the database
                db_post = self.session.query(Post).filter(Post.post_id == pid).first()
                if db_post:
                    log.debug(f"Post {pid} from channel {channel.channel_name} already exists in the database; skipping...")
                    continue  # TODO: Update post, its metrics and reactions
                db_post = Post(post_id=pid,
                               channel_id=channel.channel_id,
                               content=post['text'],
                               post_date=post['timestamp'])
                log.debug(f"Adding post {pid} from channel {channel.channel_name} to the database...")
                self.session.add(db_post)
                self.session.commit()
                # TODO: Add post metrics
                # Add mock values for now
                # class PostMetrics(Base):
                #     __tablename__ = "post_metrics"

                #     metric_id = Column(Integer, primary_key=True)
                #     post_id = Column(Integer, ForeignKey("posts.post_id"))
                #     views = Column(Integer)
                #     reposts = Column(Integer)
                #     comments = Column(Integer)
                #     links = Column(Integer)
                #     images = Column(Integer)
                #     videos = Column(Integer)
                #     recorded_date = Column(DateTime)
                db_post_metrics = PostMetrics(post_id=pid,
                                              views=123,
                                              reposts=456,
                                              comments=678,
                                              links=12,
                                              images=2,
                                              videos=0,
                                              recorded_date=datetime.now())
                self.session.add(db_post_metrics)
                self.session.commit()
                for reaction, count in post['reactions'].items():
                    db_reaction = Reaction(post_id=pid,
                                           reaction_desc=reaction,
                                           count=count)
                    log.debug(f"Adding reaction {reaction} to post {pid} from channel {channel.channel_name} to the database...")
                    self.session.add(db_reaction)
                self.session.commit()
                for cid, comment in post['comments'].items():
                    db_comment = Comment(comment_id=cid,
                                         post_id=pid,
                                         content=comment['text'],
                                         comment_date=comment['timestamp'])
                    log.debug(f"Adding comment {cid} to post {pid} from channel {channel.channel_name} to the database...")
                    self.session.add(db_comment)
            self.session.commit()
        except Exception as exc:
            log.error(f"An error occurred while adding channel \"{data['name']}\" to the database: {exc}")
            self.session.rollback()
        log.debug(f"Finished adding channel \"{data['name']}\" to the database!")

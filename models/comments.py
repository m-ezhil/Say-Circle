from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Comments(Base):
    __tablename__ = 'comments'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    comment = Column('comment', String, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column('post_id', Integer, ForeignKey('posts.id'), nullable=False)
    create_at = Column('create_at', DateTime, default=datetime.now(timezone.utc))
    active_state = Column('active_state', Integer, default=1)

    post = relationship('Posts', back_populates='comments')
    owner = relationship('Users', back_populates='comments')

    def __init__(self, comment, user_id, post_id):
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id
        self.create_at = datetime.now(timezone.utc)

    def get_dict(self):
        return {
            'comment':self.comment,
            'user_id':self.user_id,
            'post_id':self.post_id,
            'create_at':self.create_at,
            'id':self.id,
            'active_state':self.active_state
        }
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Posts(Base):
    __tablename__ = 'posts'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String, nullable=False)
    content = Column('content', String, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    create_at = Column('create_at', DateTime, default=datetime.now(timezone.utc))
    active_state = Column('active_state', Integer, default=1)

    owner = relationship('Users', back_populates='posts')
    comments = relationship('Comments', back_populates='post')

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.create_at = datetime.now(timezone.utc)

    def get_dict(self):
        return {
            'title':self.title,
            'content':self.content,
            'user_id':self.user_id,
            'owner':{'user_name':self.owner.user_name, 'user_id':self.owner.id} if self.owner else None,
            'create_at':self.create_at,
            'id':self.id,
            'active_state':self.active_state,
            'comments':[comment.get_dict() for comment in self.comments]
        }
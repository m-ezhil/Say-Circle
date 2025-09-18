from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_name = Column('user_name', String, nullable=False)
    email = Column('email', String, nullable=False,unique=True)
    password_hased = Column('password_hased', String, nullable=False)
    active_state = Column('active_state', Integer, default=1)

    posts = relationship('Posts', back_populates='owner')
    comments = relationship('Comments', back_populates='owner')

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password_hased = generate_password_hash(password)

    def get_dict(self):
        return {
            'user_name': self.user_name,
            'email':self.email,
            'id':self.id,
            'active_state':self.active_state,
            'posts':[post.get_dict() for post in self.posts]
        }
    
    def check_password(self, password):
        return check_password_hash(self.password_hased, password)
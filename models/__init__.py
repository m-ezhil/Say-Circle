from .database import create_db, and_
from .users import Users
from .posts import Posts
from .comments import Comments
from datetime import datetime
engine,session = create_db()

def add_user(user_name, email, password):
    user = session.query(Users).filter(Users.email == email).first()
    if user: return False, user.get_dict()
    new_user = Users(user_name=user_name,email=email, password=password)
    session.add(new_user)
    session.commit()
    return True, new_user.get_dict()

def get_user_by_email(email, active_state = 1):
    user = session.query(Users).where(and_(Users.active_state.in_([active_state] if active_state > -1 else [0,1]), Users.email == email)).first()
    if not user: return 
    return user.get_dict() if user else None

def get_user_by_id(user_id, active_state = 1):
    user = session.query(Users).where(and_(Users.active_state.in_([active_state] if active_state > -1 else [0,1]), Users.id == user_id)).first()
    if not user: return 
    return user.get_dict() if user else None

def is_valid_user(email, password):
    user = session.query(Users).where(and_(Users.active_state == 1, Users.email == email)).first()
    if not user: return False, None
    return user.check_password(password), user.get_dict()

def get_all_user(active_state = 1):
    users = [user.get_dict() for user in session.query(Users).where(Users.active_state.in_([active_state] if active_state > -1 else [0,1])).all()]
    if not users: return
    return users if users else []

def add_post(title, content, user_id):
    new_post = Posts(title=title ,content=content, user_id=user_id)
    session.add(new_post)
    session.commit()
    return new_post.get_dict()

def get_all_posts(active_state = 1):
    posts = session.query(Posts).where(Posts.active_state == 1).all()
    return [post.get_dict() for post in posts] if posts else []

def get_post_by_id(post_id, active_state = 1):
    post = session.query(Posts).where(and_(Posts.id == post_id, Posts.active_state.in_([active_state] if active_state > -1 else [0,1]))).first()
    if not post: return
    return post.get_dict() if post else []

def get_posts_by_user_id(user_id, active_state = 1):
    posts = session.query(Posts).where(and_(Posts.user_id == user_id, Posts.active_state.in_([active_state] if active_state > -1 else [0,1]))).all()
    if not posts: return
    return [post.get_dict() for post in posts] if posts else []

def update_post_by_id(post_id, title=None, content=None):
    post = session.query(Posts).where(and_(Posts.id == post_id, Posts.active_state == 1)).first()
    if not post: return
    if content: post.content = content
    if title: post.title = title
    session.commit()
    return post.get_dict()

def delete_post_by_id(post_id):
    post = session.query(Posts).where(and_(Posts.id == post_id, Posts.active_state == 1)).first()
    if not post: return 
    post.active_state = 0
    session.commit()
    return post.get_dict()

def add_comment(comment, post_id, user_id):
    new_comment = Comments(comment=comment, post_id=post_id, user_id=user_id)
    session.add(new_comment)
    session.commit()
    return new_comment.get_dict()

def get_all_comments(active_state=1):
    comments = session.query(Comments).where(Comments.active_state.in_([active_state] if active_state > -1 else [0,1])).all()
    return [comment.get_dict() for comment in comments] if comments else []

def get_comments_by_post_id(post_id, active_state=1):
    comments = session.query(Comments).where(and_(Comments.active_state.in_([active_state] if active_state > -1 else [0,1]), Comments.post_id == post_id)).all()
    return [comment.get_dict() for comment in comments] if comments else []

def get_comments_by_user_id(user_id, active_state=1):
    comments = session.query(Comments).where(and_(Comments.active_state.in_([active_state] if active_state > -1 else [0,1]), Comments.user_id == user_id)).all()
    return [comment.get_dict() for comment in comments] if comments else []
  
def get_comment_by_id(comment_id, active_state=1):
    comment = session.query(Comments).where(and_(Comments.active_state.in_([active_state] if active_state > -1 else [0,1]), Comments.id == comment_id)).all()
    return comment.get_dict() if comment else None

def update_comment_by_id(comment_id, content=None):
    comment = session.query(Comments).where(and_(Comments.id == comment_id, Comments.active_state == 1)).first()
    if not comment: return
    comment.comment = content
    session.commit()
    return comment.get_dict()

def delete_comment_by_id(comment_id):
    comment = session.query(Comments).where(and_(Comments.id == comment_id, Comments.active_state == 1)).first()
    if not comment: return 
    comment.active_state = 0
    session.commit()
    return comment.get_dict()



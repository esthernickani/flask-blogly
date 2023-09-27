"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

class User(db.Model):
    """Users"""
    __tablename__ = "users"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(20),
                           nullable = False,
                           unique = True)
    last_name = db.Column(db.String(20),
                           nullable = False,
                           unique = True)
    image_url = db.Column(db.String(100),
                           nullable = False,
                           default = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1200px-Default_pfp.svg.png")
    
    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User{u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    post = db.relationship('Post', backref="posts", cascade="all, delete-orphan")

"""Get now time"""
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")

class Post(db.Model):
    """Posts"""
    __tablename__ = "posts"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String,
                      nullable = False,
                      unique = True)
    content = db.Column(db.String, 
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           default = datetime.utcnow,
                           nullable = False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    def __repr__(self):
        """Show info about post"""
        p = self
        return f"<Post{p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

    
class Tag(db.Model):
    """tags"""
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.String,
                      nullable = False,
                      unique = True)
    
    def __repr__(self):
        """Show info about post"""
        t = self
        return f"<Tag{t.id} {t.name}>"
    
class PostTag(db.Model):
    """join post to tag"""
    __tablename__ = "post_tag"
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id', ondelete='CASCADE'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key = True)
    
    def __repr__(self):
        """Show info about post"""
        pt = self
        return f"<PostTag{pt.tag_id} {pt.post_id}>"
    
    
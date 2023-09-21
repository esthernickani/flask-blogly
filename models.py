"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
        return f"<User{u.id} {u.first_name} {u.last_name} {u.image_url}"
    
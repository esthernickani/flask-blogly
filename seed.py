"""Seed file to make sample data for users db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables

db.drop_all()
db.create_all()
User.query.delete()

# If table isn't empty, empty it


# Add users
alan = User(first_name = 'Alan', last_name = 'Alda')
joel = User(first_name = 'Joel', last_name = 'Burton')
jane = User(first_name = 'Jane', last_name = 'Smith')

#Add posts for Alan
first_post = Post(title = 'First Post', content = 'Oh, hai.', user_id = 1)
yet_another_post = Post(title = 'Yet Another Post', content = 'Oh, hello.', user_id = 1)
flask_is_awesome_post = Post(title = 'Flask is awesome', content = 'Flask is an awesome framework written in python', user_id = 1)

# Add new objects to session and commit

db.session.add_all([joel, alan, jane])
db.session.commit()

db.session.add_all([first_post, yet_another_post, flask_is_awesome_post])
db.session.commit()

#Add tags
fun = Tag(name= 'Fun')
more = Tag(name= 'Even more')
bloop = Tag(name= 'Bloop')
zope = Tag(name= 'Zope')

db.session.add_all([fun, more, bloop, zope])
db.session.commit()

post = Post.query.get(2)
tag = Tag.query.get(2)

post_tag = PostTag(post_id=post.id, tag_id=tag.id)
db.session.add(post_tag)
db.session.commit()


"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

# If table isn't empty, empty it


# Add users
alan = User(first_name = 'Alan', last_name = 'Alda')
joel = User(first_name = 'Joel', last_name = 'Burton')
jane = User(first_name = 'Jane', last_name = 'Smith')

# Add new objects to session and commit
with app.app_context():
    db.session.add(joel)
    db.session.add(alan)
    db.session.add(jane)
    db.session.commit()
    db.create_all()

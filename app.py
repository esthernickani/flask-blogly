"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
import pdb

app = Flask(__name__, template_folder = "templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "hellothere"
toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    """Redirect homepage"""
    return redirect("/users")

@app.route('/users')
def list_users():
    """Show list of users in db"""
    users = User.query.all()
    return render_template("base.html", users=users)

@app.route('/users/new')
def show_form():
    """Show add user form"""
    return render_template("userform.html")

@app.route('/', methods=["POST"])
def create_user():
    """Process the add form and add a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image"]

    image_url = image_url if image_url else None

    

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    pdb.set_trace()
    with app.app_context():
        db.session.add(new_user)
        db.session.commit
    
    return redirect(f"/{new_user.id}")

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show user information"""
    user = User.query.get_or_404(user_id)
    return render_template("userdetail.html", user=user)



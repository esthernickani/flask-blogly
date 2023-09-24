"""Blogly application."""

from flask import Flask, render_template, redirect, request
"""from flask_debugtoolbar import DebugToolbarExtension"""
from models import db, connect_db, User, Post
import pdb

app = Flask(__name__, template_folder = "templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)

app.config['SECRET_KEY'] = "hellothere"
"""toolbar = DebugToolbarExtension(app)"""

def get_post():
    """Get all the posts"""
    posts = Post.query.all()
    return posts

posts = get_post()

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

    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show user information"""
    user = User.query.get_or_404(user_id)
    current_user_posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template("userdetail.html", user=user, posts=current_user_posts)

@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    """Edit current user"""
    current_user = User.query.get_or_404(user_id)
    return render_template("edituser.html", current_user = current_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edit current user"""
    current_user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image"]

    first_name = first_name if first_name else current_user.first_name
    last_name = last_name if last_name else current_user.last_name
    image_url = image_url if image_url else current_user.image_url

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.image_url = image_url

    db.session.commit()

    users = User.query.all()

    return render_template("base.html", users = users)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete selected user"""
    posts_to_delete = Post.query.filter(Post.user_id == user_id).all()
    for post in posts_to_delete:
        db.session.delete(post)
    db.session.commit()

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    users = User.query.all()
    return render_template("base.html", users = users)


"""POSTS ROUTES"""
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show new post form"""
    current_user = User.query.get_or_404(user_id)
    return render_template("newpostform.html", user = current_user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post(user_id):
    """Handle new post"""
    title = request.form["title"]
    content = request.form["content"]
    user_id = user_id

    if title and content:
        new_post = Post(title = title, content = content, user_id = user_id)
        db.session.add(new_post)
        db.session.commit()

    user = User.query.get_or_404(user_id)
    current_user_posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template("userdetail.html", user=user, posts=current_user_posts)

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Get post details"""
    current_post = Post.query.get_or_404(post_id)
    current_user = User.query.get_or_404(current_post.user_id)
    user_name = f"{current_user.first_name} {current_user.last_name}"
    return render_template("postdetail.html", post = current_post, user_name = user_name)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """show post edit form"""
    current_post = Post.query.get_or_404(post_id)
    return render_template("editpostform.html", post = current_post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """handle post new info"""
    current_post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    title = title if title else current_post.title
    content = content if content else current_post.content

    current_post.title = title
    current_post.content = content

    db.session.commit()

    current_post = Post.query.get_or_404(post_id)
    current_user = User.query.get_or_404(current_post.user_id)
    user_name = f"{current_user.first_name} {current_user.last_name}"
    return render_template("postdetail.html", post = current_post, user_name = user_name)

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete selected post"""
    current_post = Post.query.get_or_404(post_id)
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    user = User.query.get_or_404(current_post.user_id)
    current_user_posts = Post.query.filter(Post.user_id == current_post.user_id).all()
    return render_template("userdetail.html", user=user, posts=current_user_posts)



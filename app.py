"""Blogly application."""

from flask import Flask, render_template, redirect, request
"""from flask_debugtoolbar import DebugToolbarExtension"""
from models import db, connect_db, User, Post, Tag, PostTag
import pdb

app = Flask(__name__, template_folder = "templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)

app.config['SECRET_KEY'] = "hellothere"
"""toolbar = DebugToolbarExtension(app)"""

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
    tags = Tag.query.all()
    return render_template("newpostform.html", user = current_user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post(user_id):
    """Handle new post"""
    title = request.form["title"]
    content = request.form["content"]
    user_id = user_id

    """check what tags were clicked"""
    tags = Tag.query.all()
    alltags = []
    for tag in tags:
        if request.form.get(f"{tag.name}") == 'on':
            alltags.append(tag)
        
    print(alltags)

    if title and content:
        new_post = Post(title = title, content = content, user_id = user_id)
        db.session.add(new_post)
        db.session.commit()

        for tag in alltags:
            new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
            db.session.add(new_post_tag)
            db.session.commit()

    user = User.query.get_or_404(user_id)
    current_user_posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template("userdetail.html", user=user, posts=current_user_posts, tags=tags)

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Get post details"""
    current_post = Post.query.get_or_404(post_id)
    current_user = User.query.get_or_404(current_post.user_id)
    user_name = f"{current_user.first_name} {current_user.last_name}"

    all_tags = []

    tags_id = PostTag.query.filter_by(post_id = current_post.id).all()
    if tags_id:
        for tag in tags_id:
            id = tag.tag_id
            tags = Tag.query.get_or_404(id)
            all_tags.append(tags)
        
        
    return render_template("postdetail.html", post = current_post, user_name = user_name, tags = all_tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """show post edit form"""
    current_post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    posttags_id = PostTag.query.filter_by(post_id = current_post.id).all()

    current_postid_tags = [posttag_id.tag_id for posttag_id in posttags_id]

    all_tags = [tag for tag in tags]
    all_tags_id = [tag.id for tag in tags]
    #if tags_id:
        #for tag in tags_id:
            #id = tag.tag_id
            #tags = Tag.query.get_or_404(id)
            #all_tags.append(tags)
    

    return render_template("editpostform.html", post = current_post, tags=all_tags, current_postid_tags=current_postid_tags)

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

    tags = Tag.query.all()
    alltags = []
    for tag in tags:
        if request.form.get(f"{tag.name}") == 'on':
            alltags.append(tag)
        else:
            PostTag.query.filter_by(post_id = current_post.id).delete()
            db.session.commit()
    
    for tag in alltags:
        tags_id = PostTag.query.filter_by(post_id = current_post.id).all()
        previous_tags = [tag.tag_id for tag in tags_id]

        if tag.id not in previous_tags:
            another_tag = PostTag(post_id=current_post.id, tag_id=tag.id)
            db.session.add(another_tag)
            db.session.commit()

    current_post = Post.query.get_or_404(post_id)
    current_user = User.query.get_or_404(current_post.user_id)
    user_name = f"{current_user.first_name} {current_user.last_name}"

    current_post_tag = []

    current_tags_id = PostTag.query.filter_by(post_id = current_post.id).all()
    if current_tags_id:
        for tag in current_tags_id:
            id = tag.tag_id
            tags = Tag.query.get_or_404(id)
            current_post_tag.append(tags)

    return render_template("postdetail.html", post = current_post, user_name = user_name, tags=current_post_tag)

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete selected post"""
    current_post = Post.query.get_or_404(post_id)
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    user = User.query.get_or_404(current_post.user_id)
    current_user_posts = Post.query.filter(Post.user_id == current_post.user_id).all()
    return render_template("userdetail.html", user=user, posts=current_user_posts)

"""Tags"""
@app.route('/tags')
def list_tags():
    """Show list of tags in db"""
    tags = Tag.query.all()
    return render_template("alltags.html", tags=tags)

@app.route('/tags/new')
def show_addtag_form():
    """Show a form to add tag"""
    return render_template("newtag.html")

@app.route('/tags/new', methods=["POST"])
def handle_add_tag():
    """Handle new tag"""
    tag_name = request.form["tagname"]

    if tag_name:
        new_tag = Tag(name = tag_name)
        db.session.add(new_tag)
        db.session.commit()

    tags = Tag.query.all()
    return render_template("alltags.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show details about each tag"""
    current_tag = Tag.query.get_or_404(tag_id)
    posttags = PostTag.query.filter_by(tag_id = tag_id).all()

    posts = []
    for posttag in posttags:
        postid = posttag.post_id
        post = Post.query.get_or_404(postid)
        posts.append(post)
    
    return render_template("tagdetail.html", posts=posts, current_tag=current_tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """show Edit tag form"""
    current_tag = Tag.query.get_or_404(tag_id)
    
    return render_template("edittag.html", tag=current_tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """handle Edit tag form"""
    current_tag = Tag.query.get_or_404(tag_id)
    tagname = request.form["tagname"]

    tagname = tagname if tagname else current_tag.name

    current_tag.name = tagname
    db.session.commit()
    tags = Tag.query.all()
    
    return render_template("alltags.html", tags=tags)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """delete a tag"""
    current_tag = Tag.query.get_or_404(tag_id)
    PostTag.query.filter(PostTag.tag_id == current_tag.id).delete()
    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()

    tags = Tag.query.all()
    return render_template("alltags.html", tags=tags)
"""Blogly application."""

from flask import Flask, render_template, session, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password123'
app.app_context().push()

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

connect_db(app)
# db.create_all()

@app.route('/')
def root():

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)

@app.route('/users')
def list_users():
    """shows list of all users - home page"""

    all_users = User.query.all()
    return render_template('users/list.html', users=all_users)

@app.route('/users/new')
def show_add_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url  = request.form['img_url']

    new_user = User(first_name = f_name, last_name = l_name, image_url = img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('users/details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """shows the edit users page"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    
    user = User.query.get(user_id)
    user.first_name = request.form['f_name']
    user.last_name = request.form['l_name']
    user.image_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def get_new_post_page(user_id):
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template(f'posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new_post(user_id):
    
    title = request.form['title']
    content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id = user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show details about a single post"""

    post = Post.query.get_or_404(post_id)


    return render_template('posts/details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def get_edit_post(post_id):
    """show edit post form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('/posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit_post(post_id):
    
    post = Post.query.get(post_id)
    
    title = request.form['title']
    content = request.form['content']
    post.title = title
    post.content = content
    
    tags_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user}')

@app.route('/tags')
def show_tags():
    """show all tags"""

    all_tags = Tag.query.all()

    return render_template('tags/all.html', tags=all_tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """show items that are assoc. with tag"""

    tag = Tag.query.get_or_404(tag_id)
    articles = tag.post

    return render_template('tags/details.html', tag=tag, posts = articles)


@app.route('/tags/new')
def show_tag_form():
    """load form to add new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def create_tag():
    
    posts_id = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(posts_id)).all()
    
    name = request.form['name']

    new_tag = Tag(name = name, post = posts)
    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tags/{new_tag.id}')

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template(tags/edit.html, tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tags_edit(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.psots = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
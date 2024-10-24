"""Blogly application."""

from flask import Flask, render_template, session, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
def redirect_all_users():

    return redirect('/users')

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
    
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img_url  = request.form['img_url']

    user = User.query.get(user_id)

    if (f_name):
        user.first_name = f_name
    if (l_name):    
        user.last_name = l_name
    if (img_url):  
        user.image_url = img_url

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
    return render_template(f'posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new_post(user_id):
    
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id = user_id)

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
    return render_template('/posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit_post(post_id):
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id)

    post.title = title
    post.content = content

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










"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, create_user, Post, create_post, Tag, create_tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'herewegoloopdyloop'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    return redirect("/users")

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def new_user():
    return render_template('newuserform.html') 

@app.route('/users/new', methods=["POST"])
def add_new_user():
    
    firstname = request.form["firstname"] #if request.form["firstname"] else None
    lastname = request.form['lastname'] #if request.form["lastname"] else None
    imageurl = request.form['imageurl'] #if request.form["imageurl"] else None

    create_user(firstname, lastname, imageurl)
    
    return redirect('/users')

@app.route('/users/<user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('user-details.html', user=user)

@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit-user-details.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def save_edit_user(user_id):
    
    firstname = request.form["firstname"]
    lastname = request.form['lastname']
    imageurl = request.form['imageurl']

    user = User.query.get_or_404(user_id)

    user.edit_user(firstname, lastname, imageurl)

    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    user.delete_user()
    
    return redirect('/users')

@app.route('/users/<user_id>/posts/new')
def posting_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post-form.html', user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):

    title = request.form['post-title']
    content = request.form['post-content']
    tags = request.form.getlist('tagcheckboxes')

    create_post(title, content, user_id, tags)

    return redirect(f"/users/{user_id}")

@app.route('/posts/<post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('show-post.html', post=post, tags=tags)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def save_edited_post(post_id):

    title = request.form['post-title']
    content = request.form['post-content']


    post = Post.query.get_or_404(post_id)
    post.edit_post(title, content)

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    post.delete_post()

    return redirect(f"/users/{user_id}")

@app.route('/tags')
def show_tags():

    tags = Tag.query.all()

    return render_template('showtags.html', tags=tags)

@app.route('/tags/<tag_id>')
def show_tag_details(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def new_tag():

    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():

    name = request.form['tag-name']

    create_tag(name)

    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=['POST'])
def save_edited_tag(tag_id):

    name = request.form['tag-name']


    tag = Tag.query.get_or_404(tag_id)
    tag.edit_tag(name=name)

    return redirect('/tags')


@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    tag.delete_tag()

    return redirect(f"/tags")



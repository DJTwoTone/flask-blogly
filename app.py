"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User

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
    
    firstname = request.form["firstname"] if request.form["firstname"] else None
    lastname = request.form['lastname'] if request.form["lastname"] else None
    imageurl = request.form['imageurl'] if request.form["imageurl"] else None

    User.create_user(firstname, lastname, imageurl)
    
    return redirect('/users')

@app.route('/users/<user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('user-details.html', user=user)

@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit-user-details.html', user=user)

# @app.route('/users/<user_id>/edit', methods=['POST'])
# def save_edit_user(user_id):
    
#     firstname = request.form["fname"]
#     lastname = request.form['lname']
#     imageurl = request.form['imurl']





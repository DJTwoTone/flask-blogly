from unittest import TestCase

from app import app

from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()



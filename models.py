"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """A class for users"""

    __tablename__ = 'users'
    __table_args__ = (db.CheckConstraint(
            'first_name IS NOT NULL OR last_name IS NOT NULL'
                                    ), db.UniqueConstraint('first_name', 'last_name')
                        )


    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String,
                            nullable=False,
                            default='https://images.pexels.com/photos/4273375/pexels-photo-4273375.jpeg')


    
    def edit_user(self, firstname, lastname, imageurl):
        self.first_name = firstname
        self.last_name = lastname
        self.image_url = imageurl
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    """A class for posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=true, autoincrement=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


def create_user(firstname, lastname, imageurl):
    new_user = User(first_name=firstname, last_name=lastname, image_url=imageurl)
    db.session.add(new_user)
    db.session.commit()
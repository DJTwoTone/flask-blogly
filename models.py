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
    posts = db.relationship('Post', backref='user')

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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    

    def edit_post(self, title, content):
        self.title = title
        self.content = content
        db.session.commit()

    def delete_post(self):

        db.session.delete(self)
        db.session.commit()

class Tag(db.Model):
    """A class for tags to be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', secondary='posttags', backref='tags')
    

    def edit_tag(self, name):
        self.name = name
        db.session.commit()

    def delete_tag(self):
        db.session.delete(self)
        db.session.commit()

        
class PostTag(db.Model):
    """A class for the post/tag join table"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)



def create_user(firstname, lastname, imageurl):
    new_user = User(first_name=firstname, last_name=lastname, image_url=imageurl)
    db.session.add(new_user)
    db.session.commit()

def create_post(title, content, user_id, tags):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    
    for tag in tags:
        id = int(tag)
        post.tags.append(Tag.query.get_or_404(id))
    db.session.commit()

def create_tag(name):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

"""Models for Blogly."""


class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)

    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=False)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def formatted_date(self):
        """get a formatted date"""
        return self.created_at.strftime("%c")


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
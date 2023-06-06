"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'helpmeiampanicking'
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)
with app.app_context():
  connect_db(app)
  db.create_all()

DEFAULT_IMAGE_URL ="https://clipart-library.com/new_gallery/236-2365757_waluigi-sticker-waluigi-face-transparent.png"

# this is a good default image

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def index():

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def new_user_form():
    """new user creation form"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or DEFAULT_IMAGE_URL)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user page"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """edit user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Add user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Delete selected user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
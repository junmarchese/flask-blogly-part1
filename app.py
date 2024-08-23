"""Blogly application."""

from flask import Flask, redirect, render_template, request, url_for
from models import db, connect_db, User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    connect_db(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

# call this only if/when testing app
# app = create_app(test_config=True)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/')
def home():
    """Redirect to list of users."""
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    """List all users."""
    users = User.query.all()
    return render_template('users_list.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    """Add a new user."""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('list_users'))
    
    return render_template('new_user.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Show edit page for a user and allow existing user to make edits."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.commit()
        return redirect(url_for('show_user', user_id=user.id))
    
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))



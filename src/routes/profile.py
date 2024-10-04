import random
import string
import hashlib
from datetime import datetime
from flask import render_template, redirect, url_for, request, blueprints, flash, blueprints
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.config import app, db

profile_bp = blueprints.Blueprint('profile', __name__)

def get_gravatar_url(email, size=200):
    # Create an MD5 hash of the email address
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"


# View Profile Route
@app.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """
    This route displays the user's profile information.
    """
    user = current_user  # Get the currently logged-in user
    user.profile_picture_url = get_gravatar_url(user.email)
    return render_template('users/view_profile.html', user=user)

def generate_random_password():
    """
    Generate a random password for the user.
    """
    password_length = 12
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(password_length))

# Change Password Route
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    This route allows users to change their password.
    """
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if the old password is correct
        if not check_password_hash(current_user.password, old_password):
            flash('Old password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        # Check if the new password matches the confirmation
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password'))

        # Update the user's password
        current_user.password = generate_password_hash(new_password)
        current_user.last_updated = datetime.utcnow()
        current_user.password_last_changed = datetime.utcnow()
        current_user.save()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('view_profile'))

    return render_template('users/change_password.html', user=current_user,
                            random_password=generate_random_password())

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    This route allows the user to edit their profile information.
    """
    user = current_user  # Get the currently logged-in user

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_username = request.form['username']
        new_email = request.form['email']
        profession = request.form['profession']
        receive_email_alerts = 'receive_email_alerts' in request.form

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.username = new_username
        user.email = new_email
        user.profession = profession
        user.receive_email_alerts = receive_email_alerts
        user.last_updated = datetime.utcnow()

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile'))

    return render_template('users/edit_profile.html', user=user)


# delete_user() function for self-deletion
@app.route('/delete_user', methods=['GET'])
@login_required
def delete_user_self():
    """
    This route allows users to delete their own account.
    """
    user = current_user
    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted.', 'success')
    return redirect(url_for('login'))

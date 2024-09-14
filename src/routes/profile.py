from flask import render_template, redirect, url_for, request, blueprints, flash, blueprints
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.config import app, db

profile_bp = blueprints.Blueprint('profile', __name__)

# View Profile Route
@app.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """
    This route displays the user's profile information.
    """
    user = current_user  # Get the currently logged-in user
    return render_template('users/view_profile.html', user=user)

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
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('view_profile'))

    return render_template('users/change_password.html', user=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    This route allows the user to edit their profile information.
    """
    user = current_user  # Get the currently logged-in user

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        profession = request.form['profession']
        receive_email_alerts = 'receive_email_alerts' in request.form

        # Update user information
        user.username = new_username
        user.email = new_email
        user.profession = profession
        user.receive_email_alerts = receive_email_alerts

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile'))

    return render_template('users/edit_profile.html', user=user)

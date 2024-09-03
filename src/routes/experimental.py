from flask import render_template, redirect, url_for, request, flash, blueprints
from flask_login import current_user
from src.config import app, db
from src.models import DashboardCard

experimental_bp = blueprints.Blueprint("experimental", __name__)

@app.route('/update_card', methods=['GET', 'POST'])
def update_card():
    # Fetch cards for the current user
    user_cards = DashboardCard.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        card_id = request.form.get('card_id')
        card = DashboardCard.query.get_or_404(card_id)

        card.card_name = request.form['card_name']
        card.card_description = request.form['card_description']
        card.card_color = request.form['card_color']
        card.card_length = request.form['card_length']
        card.card_position = int(request.form['card_position'])
        card.card_enabled = 'card_enabled' in request.form

        db.session.commit()
        flash('Card updated successfully!', 'success')
        return redirect(url_for('update_card'))  # Redirect to the same page to reflect changes

    return render_template('cards/update_card.html', user_cards=user_cards)


@app.route('/experimental')
def experimental():
    # Fetch cards for the current user
    card_settings = DashboardCard.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard/experimental.html', card_settings=card_settings)

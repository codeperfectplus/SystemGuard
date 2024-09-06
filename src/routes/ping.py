import datetime
from threading import Timer
from flask import render_template, request, redirect, url_for, blueprints, flash
from src.config import app, db
from src.models.ping import Website
import requests

ping_bp = blueprints.Blueprint('ping', __name__)

# Route to view and add websites
@app.route('/ping')
def ping_website():
    websites = Website.query.all()
    return render_template('ping/ping.html', websites=websites)

# Route to add a website
@app.route('/add_website', methods=['POST'])
def add_website():
    name = request.form['name']
    ping_period = int(request.form['ping_period'])
    website = Website(name=name, ping_period=ping_period, is_ping=True)
    db.session.add(website)
    db.session.commit()
    return redirect(url_for('ping_website'))

@app.route('/remove_website/<int:website_id>', methods=['POST'])
def remove_website(website_id):
    website = Website.query.get_or_404(website_id)
    db.session.delete(website)
    db.session.commit()
    flash('Website removed successfully!', 'danger')
    return redirect(url_for('ping_website'))

@app.route('/edit_website/<int:website_id>', methods=['GET', 'POST'])
def edit_website(website_id):
    website = Website.query.get_or_404(website_id)
    if request.method == 'POST':
        website.name = request.form['name']
        website.ping_period = int(request.form['ping_period'])
        db.session.commit()
        flash('Website updated successfully!', 'success')
        return redirect(url_for('ping_website'))
    return render_template('ping/edit_website.html', website=website)

# Route to toggle pinging status
@app.route('/toggle_ping/<int:website_id>')
def toggle_ping(website_id):
    website = Website.query.get_or_404(website_id)
    website.is_ping = not website.is_ping
    db.session.commit()
    return redirect(url_for('ping_website'))

# Function to ping websites periodically
def ping_websites():
    with app.app_context():
        websites = Website.query.filter_by(is_ping=True).all()
        for website in websites:
            print(f'Pinging {website.name}...')
            try:
                response = requests.get(website.name, timeout=10)
                website.last_ping_timestamp = datetime.datetime.now()
                if response.status_code == 200:
                    website.last_status = 'UP'
                else:
                    website.last_status = 'DOWN'
            except requests.RequestException:
                website.last_status = 'Something went wrong'

            db.session.commit()

        # Schedule next ping after the minimum interval period
        min_interval = min([w.ping_period for w in websites]) if websites else 60
        Timer(min_interval, ping_websites).start()

# Start pinging periodically after server starts
ping_websites()

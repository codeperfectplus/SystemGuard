import datetime
from threading import Timer
from flask import render_template, request, redirect, url_for, blueprints, flash
from src.config import app, db
from src.models.monitored_website import MonitoredWebsite
from flask_login import login_required
import requests

ping_bp = blueprints.Blueprint('ping', __name__)

# Route to view and add websites
@app.route('/monitor_websites')
@login_required
def monitor_websites():
    websites = MonitoredWebsite.query.all()
    return render_template('ping/ping.html', websites=websites)

# Route to add a website
@app.route('/add_monitored_website', methods=['POST'])
@login_required
def add_website():
    name = request.form['name']
    ping_interval = int(request.form['ping_interval'])
    email_alerts_enabled = request.form.get('email_alerts_enabled') == 'on'
    website = MonitoredWebsite(name=name, ping_interval=ping_interval, is_ping_active=True, email_alerts_enabled=email_alerts_enabled)
    db.session.add(website)
    db.session.commit()
    return redirect(url_for('monitor_websites'))

@app.route('/delete_monitored_website/<int:website_id>', methods=['POST'])
@login_required
def remove_website(website_id):
    website = MonitoredWebsite.query.get_or_404(website_id)
    db.session.delete(website)
    db.session.commit()
    flash('Website removed successfully!', 'danger')
    return redirect(url_for('monitor_websites'))

@app.route('/edit_monitored_website/<int:website_id>', methods=['GET', 'POST'])
def edit_website(website_id):
    website = MonitoredWebsite.query.get_or_404(website_id)
    if request.method == 'POST':
        website.name = request.form['name']
        website.ping_interval = int(request.form['ping_interval'])
        db.session.commit()
        flash('Website updated successfully!', 'success')
        return redirect(url_for('monitor_websites'))
    return render_template('ping/edit_website.html', website=website)

# Route to toggle pinging status
@app.route('/toggle_ping_status/<int:website_id>')
@login_required
def toggle_ping(website_id):
    website = MonitoredWebsite.query.get_or_404(website_id)
    website.is_ping_active = not website.is_ping_active
    db.session.commit()
    return redirect(url_for('monitor_websites'))

@app.route('/toggle_email_alerts/<int:website_id>')
@login_required
def toggle_emaail_alerts(website_id):
    website = MonitoredWebsite.query.get_or_404(website_id)
    website.email_alerts_enabled = not website.email_alerts_enabled
    db.session.commit()
    return redirect(url_for('monitor_websites'))

# Function to ping websites periodically
def start_website_monitoring():
    with app.app_context():
        websites = MonitoredWebsite.query.filter_by(is_ping_active=True).all()
        for website in websites:
            print(f'Pinging {website.name}...')
            try:
                response = requests.get(website.name, timeout=10)
                website.last_ping_time = datetime.datetime.now()
                website.ping_status_code = response.status_code
                if response.status_code == 200:
                    website.ping_status = 'UP'
                else:
                    website.ping_status = 'DOWN'
            except requests.RequestException:
                website.ping_status = 'Something went wrong'

            db.session.commit()

        # Schedule next ping after the minimum interval period
        min_interval = min([w.ping_interval for w in websites]) if websites else 60
        Timer(min_interval, monitor_websites).start()

# Start pinging periodically after server starts
start_website_monitoring()

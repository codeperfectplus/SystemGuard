import datetime
from threading import Timer
from flask import render_template, request, redirect, url_for, blueprints, flash
from src.config import app, db
from src.models.monitored_website import MonitoredWebsite
from flask_login import login_required
import requests

ping_bp = blueprints.Blueprint('ping', __name__)

def time_ago(ping_time, current_time):
    """
    Calculate the time difference between the current time and the ping time.
    Return a human-readable format like '1 min ago' or '30 seconds ago'.
    
    Args:
        ping_time (datetime): The last ping time.
        current_time (datetime): The current time.
    
    Returns:
        str: A formatted string representing the time ago.
    """
    if not ping_time:
        return "Never"

    # Calculate the difference in seconds
    time_diff = (current_time - ping_time).total_seconds()
    
    if time_diff <= 60:
        return f"{int(time_diff)} seconds ago"
    if time_diff <= 3600:
        return f"{int(time_diff // 60)} min ago"
    if time_diff <= 86400:
        return f"{int(time_diff // 3600)} hours ago"
    else:
        # Fallback to formatted datetime if over a day
        return ping_time.strftime('%Y-%m-%d %H:%M:%S')

# Route to view and add websites
@app.route('/monitor_websites')
@login_required
def monitor_websites():
    websites = MonitoredWebsite.query.all()
    current_time = datetime.datetime.now()
    for website in websites:
        website.last_ping_time_ago = time_ago(website.last_ping_time, current_time)
    return render_template('ping/ping.html', websites=websites)

# Route to add a website
@app.route('/add_monitored_website', methods=['POST'])
@login_required
def add_website():
    name = request.form['name']
    ping_interval = int(request.form['ping_interval'])
    email_address = request.form['email_address']
    email_alerts_enabled = request.form.get('email_alerts_enabled') == 'on'
    website = MonitoredWebsite(name=name, ping_interval=ping_interval,
                               email_address=email_address, 
                               is_ping_active=True, 
                               email_alerts_enabled=email_alerts_enabled)
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
        website.email_alerts_enabled = request.form.get('email_alerts_enabled') == 'on'
        website.email_address = request.form['email_address']
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
def toggle_email_alerts(website_id):
    website = MonitoredWebsite.query.get_or_404(website_id)
    website.email_alerts_enabled = not website.email_alerts_enabled
    db.session.commit()
    return redirect(url_for('monitor_websites'))

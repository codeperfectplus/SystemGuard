from flask import Flask, render_template, request, redirect, url_for, flash, blueprints
from src.config import db, app
from src.models import NotificationSettings

webhooks_bp = blueprints.Blueprint("webhooks", __name__)

@app.route('/update-webhooks', methods=['GET', 'POST'])
def update_webhooks():
    # Fetch the first (or any) existing webhook settings from the database
    webhook_settings = NotificationSettings.query.first()
    
    if request.method == 'POST':
        slack_webhook_url = request.form.get('slack_webhook_url')
        discord_webhook_url = request.form.get('discord_webhook_url')
        teams_webhook_url = request.form.get('teams_webhook_url')
        
        # Check if webhook settings exist, if not create a new entry
        if not webhook_settings:
            webhook_settings = NotificationSettings(
                slack_webhook_url=slack_webhook_url,
                discord_webhook_url=discord_webhook_url,
                teams_webhook_url=teams_webhook_url
            )
            db.session.add(webhook_settings)
        else:
            # Update the existing webhook URLs
            webhook_settings.slack_webhook_url = slack_webhook_url
            webhook_settings.discord_webhook_url = discord_webhook_url
            webhook_settings.teams_webhook_url = teams_webhook_url
        
        webhook_settings.save()
        flash('Webhook URLs updated successfully!', 'success')
        return redirect(url_for('update_webhooks'))

    return render_template('other/update_webhooks.html', webhook_settings=webhook_settings)

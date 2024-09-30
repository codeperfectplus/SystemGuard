from flask import Flask, render_template, request, redirect, url_for, flash, blueprints
from src.config import db, app
from src.models import NotificationSettings, GeneralSettings

webhooks_bp = blueprints.Blueprint("webhooks", __name__)


@app.route("/update-webhooks", methods=["GET", "POST"])
def update_webhooks():
    # Fetch existing webhook and general settings from the database
    webhook_settings = NotificationSettings.query.first()
    general_settings = GeneralSettings.query.first()

    # Default to enabling all alerts if the general settings are missing
    enable_alerts = general_settings.enable_alerts

    if request.method == "POST":
        # Fetch the submitted webhook URLs and alert enable states from the form
        slack_webhook_url = request.form.get("slack_webhook_url")
        discord_webhook_url = request.form.get("discord_webhook_url")
        teams_webhook_url = request.form.get("teams_webhook_url")
        google_chat_webhook_url = request.form.get("google_chat_webhook_url")
        # telegram_webhook_url = request.form.get("telegram_webhook_url")
        # telegram_chat_id = request.form.get("telegram_chat_id")

        is_email_alert_enabled = request.form.get("is_email_alert_enabled") == "on"
        is_slack_alert_enabled = request.form.get("is_slack_alert_enabled") == "on"
        is_discord_alert_enabled = request.form.get("is_discord_alert_enabled") == "on"
        is_teams_alert_enabled = request.form.get("is_teams_alert_enabled") == "on"
        is_google_chat_alert_enabled = request.form.get("is_google_chat_alert_enabled") == "on"
        # is_telegram_alert_enabled = request.form.get("is_telegram_alert_enabled") == "on"
        
        enable_alerts = request.form.get("enable_alerts") == "on"

        # If "Enable All Alerts" is turned off, disable all individual alerts
        if not enable_alerts:
            is_email_alert_enabled = False
            is_slack_alert_enabled = False
            is_discord_alert_enabled = False
            is_teams_alert_enabled = False
            is_google_chat_alert_enabled = False
            # is_telegram_alert_enabled = False

        # Update and save the general settings
        if not general_settings:
            general_settings = GeneralSettings(enable_alerts=enable_alerts)
            db.session.add(general_settings)
        else:
            general_settings.enable_alerts = enable_alerts
        general_settings.save()

        # Update or create new webhook settings
        if not webhook_settings:
            webhook_settings = NotificationSettings(
                slack_webhook_url=slack_webhook_url,
                discord_webhook_url=discord_webhook_url,
                teams_webhook_url=teams_webhook_url,
                google_chat_webhook_url=google_chat_webhook_url,
                # telegram_webhook_url=telegram_webhook_url,
                # telegram_chat_id=telegram_chat_id,
                is_email_alert_enabled=is_email_alert_enabled,
                is_slack_alert_enabled=is_slack_alert_enabled,
                is_discord_alert_enabled=is_discord_alert_enabled,
                is_teams_alert_enabled=is_teams_alert_enabled,
                is_google_chat_alert_enabled=is_google_chat_alert_enabled,
                # is_telegram_alert_enabled=is_telegram_alert_enabled,
            )
            db.session.add(webhook_settings)
        else:
            # Update the existing webhook URLs and alert settings
            webhook_settings.slack_webhook_url = slack_webhook_url
            webhook_settings.discord_webhook_url = discord_webhook_url
            webhook_settings.teams_webhook_url = teams_webhook_url
            webhook_settings.google_chat_webhook_url = google_chat_webhook_url
            # webhook_settings.telegram_webhook_url = telegram_webhook_url
            # webhook_settings.telegram_chat_id = telegram_chat_id
            webhook_settings.is_email_alert_enabled = is_email_alert_enabled
            webhook_settings.is_slack_alert_enabled = is_slack_alert_enabled
            webhook_settings.is_discord_alert_enabled = is_discord_alert_enabled
            webhook_settings.is_teams_alert_enabled = is_teams_alert_enabled
            webhook_settings.is_google_chat_alert_enabled = is_google_chat_alert_enabled
            # webhook_settings.is_telegram_alert_enabled = is_telegram_alert_enabled

        webhook_settings.save()

        flash("Webhook settings updated successfully!", "success")
        return redirect(url_for("update_webhooks"))

    return render_template(
        "other/update_webhooks.html",
        webhook_settings=webhook_settings,
        enable_alerts=enable_alerts
    )

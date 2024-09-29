from flask import Flask, render_template, request, redirect, url_for, flash, blueprints
from src.config import db, app
from src.models import NotificationSettings

webhooks_bp = blueprints.Blueprint("webhooks", __name__)


@app.route("/update-webhooks", methods=["GET", "POST"])
def update_webhooks():
    # Fetch the first (or any) existing webhook settings from the database
    webhook_settings = NotificationSettings.query.first()

    if request.method == "POST":
        slack_webhook_url = request.form.get("slack_webhook_url")
        discord_webhook_url = request.form.get("discord_webhook_url")
        teams_webhook_url = request.form.get("teams_webhook_url")
        google_chat_webhook_url = request.form.get("google_chat_webhook_url")
        telegram_webhook_url = request.form.get("telegram_webhook_url")
        telegram_chat_id = request.form.get("telegram_chat_id")

        is_email_alert_enabled = request.form.get("is_email_alert_enabled") == "on"
        is_slack_alert_enabled = request.form.get("is_slack_alert_enabled") == "on"
        is_discord_alert_enabled = request.form.get("is_discord_alert_enabled") == "on"
        is_teams_alert_enabled = request.form.get("is_teams_alert_enabled") == "on"
        is_google_chat_alert_enabled = (
            request.form.get("is_google_chat_alert_enabled") == "on"
        )
        is_telegram_alert_enabled = (
            request.form.get("is_telegram_alert_enabled") == "on"
        )

        # Check if webhook settings exist, if not create a new entry
        if not webhook_settings:
            webhook_settings = NotificationSettings(
                slack_webhook_url=slack_webhook_url,
                discord_webhook_url=discord_webhook_url,
                teams_webhook_url=teams_webhook_url,
                google_chat_webhook_url=google_chat_webhook_url,
                telegram_webhook_url=telegram_webhook_url,
                telegram_chat_id=telegram_chat_id,
                is_email_alert_enabled=is_email_alert_enabled,
                is_slack_alert_enabled=is_slack_alert_enabled,
                is_discord_alert_enabled=is_discord_alert_enabled,
                is_teams_alert_enabled=is_teams_alert_enabled,
                is_google_chat_alert_enabled=is_google_chat_alert_enabled,
                is_telegram_alert_enabled=is_telegram_alert_enabled,
            )
            db.session.add(webhook_settings)
        else:
            # Update the existing webhook URLs
            webhook_settings.slack_webhook_url = slack_webhook_url
            webhook_settings.discord_webhook_url = discord_webhook_url
            webhook_settings.teams_webhook_url = teams_webhook_url
            webhook_settings.google_chat_webhook_url = google_chat_webhook_url
            webhook_settings.telegram_webhook_url = telegram_webhook_url
            webhook_settings.telegram_chat_id = telegram_chat_id
            webhook_settings.is_email_alert_enabled = is_email_alert_enabled
            webhook_settings.is_slack_alert_enabled = is_slack_alert_enabled
            webhook_settings.is_discord_alert_enabled = is_discord_alert_enabled
            webhook_settings.is_teams_alert_enabled = is_teams_alert_enabled
            webhook_settings.is_google_chat_alert_enabled = is_google_chat_alert_enabled
            webhook_settings.is_telegram_alert_enabled = is_telegram_alert_enabled

        webhook_settings.save()
        flash("Webhook URLs updated successfully!", "success")
        return redirect(url_for("update_webhooks"))

    return render_template(
        "other/update_webhooks.html", webhook_settings=webhook_settings
    )

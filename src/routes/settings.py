import datetime
from flask import render_template, request, flash, blueprints, redirect, url_for
from src.config import app, db
from src.models import DashboardSettings, User
from flask_login import login_required, current_user
from src.utils import render_template_from_file
from src.scripts.email_me import send_smpt_email

settings_bp = blueprints.Blueprint("settings", __name__)



@app.route('/settings/speedtest', methods=['GET', 'POST'])
@login_required
def speedtest_settings():
    settings = DashboardSettings.query.first()  # Retrieve settings from DB
    if request.method == 'POST':
        settings.speedtest_cooldown = request.form.get('speedtest_cooldown')
        settings.number_of_speedtests = request.form.get('number_of_speedtests')
        db.session.commit()
        flash('Speedtest settings updated successfully!', 'success')
        return redirect(url_for('speedtest_settings'))
    return render_template('speedtest_settings.html', settings=settings)

@app.route('/settings/general', methods=['GET', 'POST'])
@login_required
def general_settings():
    settings = DashboardSettings.query.first()  # Retrieve settings from DB
    if request.method == 'POST':
        settings.timezone = request.form.get('timezone')
        settings.enable_cache = 'enable_cache' in request.form
        settings.enable_alerts = 'enable_alerts' in request.form
        admin_emails = [user.email for user in User.query.filter_by(user_level="admin", receive_email_alerts=True).all()]
        if admin_emails:
            subject = "SystemGuard Server Started"
            context = {
                "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "notifications_enabled": settings.enable_alerts,
                "current_user": current_user.username
            }
            html_body = render_template_from_file("src/templates/email_templates/notification_alert.html", **context)
            print("Notification enabled:", settings.enable_alerts)
            send_smpt_email(admin_emails, subject, html_body, is_html=True, bypass_alerts=True)
        db.session.commit()
        flash('General settings updated successfully!', 'success')
        return redirect(url_for('general_settings'))
    return render_template('general_settings.html', settings=settings)

@app.route('/settings/feature-toggles', methods=['GET', 'POST'])
@login_required
def feature_toggles():
    settings = DashboardSettings.query.first()  # Retrieve settings from DB
    if request.method == 'POST':
        settings.is_cpu_info_enabled = 'is_cpu_info_enabled' in request.form
        settings.is_memory_info_enabled = 'is_memory_info_enabled' in request.form
        settings.is_disk_info_enabled = 'is_disk_info_enabled' in request.form
        settings.is_network_info_enabled = 'is_network_info_enabled' in request.form
        settings.is_process_info_enabled = 'is_process_info_enabled' in request.form
        db.session.commit()
        flash('Feature toggles updated successfully!', 'success')
        return redirect(url_for('feature_toggles'))
    return render_template('feature_toggles.html', settings=settings)

@app.route('/settings/card-toggles', methods=['GET', 'POST'])
@login_required
def card_toggles():
    settings = DashboardSettings.query.first()  # Retrieve settings from DB
    if request.method == 'POST':
        settings.is_user_card_enabled = 'is_user_card_enabled' in request.form
        settings.is_server_card_enabled = 'is_server_card_enabled' in request.form
        settings.is_battery_card_enabled = 'is_battery_card_enabled' in request.form
        settings.is_cpu_core_card_enabled = 'is_cpu_core_card_enabled' in request.form
        settings.is_cpu_usage_card_enabled = 'is_cpu_usage_card_enabled' in request.form
        settings.is_cpu_temp_card_enabled = 'is_cpu_temp_card_enabled' in request.form
        settings.is_dashboard_memory_card_enabled = 'is_dashboard_memory_card_enabled' in request.form
        settings.is_memory_usage_card_enabled = 'is_memory_usage_card_enabled' in request.form
        settings.is_disk_usage_card_enabled = 'is_disk_usage_card_enabled' in request.form
        settings.is_system_uptime_card_enabled = 'is_system_uptime_card_enabled' in request.form
        settings.is_network_statistic_card_enabled = 'is_network_statistic_card_enabled' in request.form
        settings.is_speedtest_enabled = 'is_speedtest_enabled' in request.form
        db.session.commit()
        flash('Card toggles updated successfully!', 'success')
        return redirect(url_for('card_toggles'))
    return render_template('card_toggles.html', settings=settings)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        flash("User level for this account is: " + current_user.user_level, "danger")
        flash("Please contact your administrator for more information.", "danger")
        return render_template("error/permission_denied.html")

    # Fetch the settings from the database
    settings = DashboardSettings.query.first()

    if settings:
        if request.method == "POST":
            # Update settings only if the form field is provided, otherwise keep the current value
            if "speedtest_cooldown" in request.form:
                settings.speedtest_cooldown = int(request.form["speedtest_cooldown"])
            if "number_of_speedtests" in request.form:
                settings.number_of_speedtests = int(request.form["number_of_speedtests"])
            if "timezone" in request.form:
                settings.timezone = request.form["timezone"]
            settings.enable_cache = "enable_cache" in request.form

            # Feature settings
            settings.is_cpu_info_enabled = "is_cpu_info_enabled" in request.form
            settings.is_memory_info_enabled = "is_memory_info_enabled" in request.form
            settings.is_disk_info_enabled = "is_disk_info_enabled" in request.form
            settings.is_network_info_enabled = "is_network_info_enabled" in request.form
            settings.is_process_info_enabled = "is_process_info_enabled" in request.form

            # Card settings
            settings.is_user_card_enabled = "is_user_card_enabled" in request.form
            settings.is_server_card_enabled = "is_server_card_enabled" in request.form
            settings.is_battery_card_enabled = "is_battery_card_enabled" in request.form
            settings.is_cpu_core_card_enabled = "is_cpu_core_card_enabled" in request.form
            settings.is_cpu_usage_card_enabled = "is_cpu_usage_card_enabled" in request.form
            settings.is_cpu_temp_card_enabled = "is_cpu_temp_card_enabled" in request.form
            settings.is_dashboard_memory_card_enabled = "is_dashboard_memory_card_enabled" in request.form
            settings.is_memory_usage_card_enabled = "is_memory_usage_card_enabled" in request.form
            settings.is_disk_usage_card_enabled = "is_disk_usage_card_enabled" in request.form
            settings.is_system_uptime_card_enabled = "is_system_uptime_card_enabled" in request.form
            settings.is_network_statistic_card_enabled = "is_network_statistic_card_enabled" in request.form
            settings.is_speedtest_enabled = "is_speedtest_enabled" in request.form

            # Commit the changes to the database
            db.session.commit()
            flash("Settings updated successfully!", "success")

        return render_template("settings.html", settings=settings)

import datetime
from flask import render_template, blueprints, jsonify, redirect, url_for
from flask_login import login_required, current_user

from src.config import app
from src.models import NetworkSpeedTestResult, UserDashboardSettings, UserCardSettings
from src.utils import datetimeformat, get_system_info

dashboard_bp = blueprints.Blueprint("dashboard", __name__)

@app.route("/", methods=["GET"])
@login_required
def dashboard():
    # if user is not authenticated, redirect to login page
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    user_id = current_user.id if current_user.is_authenticated else 0
    user_dashboard_settings = UserDashboardSettings.query.filter_by(user_id=user_id).first()
    system_info = get_system_info()

    # Fetch the last speedtest result
    speedtest_cooldown_time = datetime.datetime.now() - datetime.timedelta(minutes=user_dashboard_settings.speedtest_cooldown)
    recent_speedtest_results = NetworkSpeedTestResult.query.filter(
        NetworkSpeedTestResult.timestamp > speedtest_cooldown_time
    ).all()
    last_speedtest_timestamp = (
        datetimeformat(recent_speedtest_results[-1].timestamp) if recent_speedtest_results else None
    )

    if recent_speedtest_results:
        latest_result = recent_speedtest_results[-1]
        
        
        next_test_time = latest_result.timestamp + datetime.timedelta(
            minutes=user_dashboard_settings.speedtest_cooldown
        )
        remaining_time_for_next_test = round(
            (next_test_time - datetime.datetime.now()).total_seconds() / 60
        )
        speedtest_result = {
            "download_speed": latest_result.download_speed,
            "upload_speed": latest_result.upload_speed,
            "ping": latest_result.ping,
            "source": "Database",
            "show_prompt": False,
            "remaining_time_for_next_test": remaining_time_for_next_test,
        }
    else:
        # No recent results, prompt to perform a test
        speedtest_result = {
            "download_speed": None,
            "upload_speed": None,
            "ping": None,
            "source": None,
            "show_prompt": True,
            "remaining_time_for_next_test": None,
        }
    
    return render_template(
            "dashboard/developer.html",
            system_info=system_info,
            speedtest_result=speedtest_result,
            last_timestamp=last_speedtest_timestamp,
            current_user=current_user,
        )

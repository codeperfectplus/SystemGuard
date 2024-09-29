import os
import datetime
from flask import render_template, Blueprint
from flask_login import current_user
from src.config import app, db
from src.models import UserDashboardSettings, NetworkSpeedTestResult
from src.utils import run_speedtest, render_template_from_file, ROOT_DIR
from src.alert_manager import send_smtp_email
from src.config import get_app_info
from src.routes.helper.common_helper import admin_required

speedtest_bp = Blueprint("speedtest", __name__)

@app.route("/speedtest")
@admin_required
def speedtest():
    user_dashboard_settings = UserDashboardSettings.query.first()
    speedtest_cooldown_duration = user_dashboard_settings.speedtest_cooldown
    required_speedtest_count = user_dashboard_settings.number_of_speedtests

    cooldown_threshold_time = datetime.datetime.now() - datetime.timedelta(
        minutes=speedtest_cooldown_duration
    )

    recent_speedtest_results = NetworkSpeedTestResult.query.filter(
        NetworkSpeedTestResult.timestamp > cooldown_threshold_time
    ).all()

    if len(recent_speedtest_results) < required_speedtest_count:
        current_speedtest_result = run_speedtest()

        if current_speedtest_result["status"] == "Error":
            return render_template(
                "error/speedtest_error.html", error=current_speedtest_result["message"]
            )

        if current_speedtest_result:
            new_speedtest_record = NetworkSpeedTestResult(
                download_speed=current_speedtest_result["download_speed"],
                upload_speed=current_speedtest_result["upload_speed"],
                ping=current_speedtest_result["ping"],
            )
            db.session.add(new_speedtest_record)
            db.session.commit()

            receiver_email = current_user.email
            subject = "Speedtest Result"
            context = {
                "speedtest_result": current_speedtest_result,
                "title": get_app_info()["title"],
            }
            speedtest_result_template = os.path.join(
                ROOT_DIR, "src/templates/email_templates/speedtest_result.html"
            )
            email_body = render_template_from_file(speedtest_result_template, **context)
            send_smtp_email(receiver_email, subject, email_body, is_html=True)

            return render_template(
                "other/speedtest_result.html",
                speedtest_result=current_speedtest_result,
                source="Actual Test",
            )
    else:
        latest_speedtest_record = recent_speedtest_results[-1]
        next_test_time = latest_speedtest_record.timestamp + datetime.timedelta(
            minutes=speedtest_cooldown_duration
        )
        remaining_time_for_next_test = round(
            (next_test_time - datetime.datetime.now()).total_seconds() / 60
        )

        return render_template(
            "other/speedtest_result.html",
            speedtest_result=latest_speedtest_record,
            source="Database",
            next_test_time=next_test_time,
            remaining_time_for_next_test=remaining_time_for_next_test,
        )

import datetime
from flask import render_template, blueprints
from flask_login import login_required, current_user
from src.config import app, db
from src.models import DashboardSettings, SpeedTestResult
from src.utils import run_speedtest, render_template_from_file
from src.scripts.email_me import send_email

speedtest_bp = blueprints.Blueprint("speedtest", __name__)

@app.route("/speedtest")
@login_required
def speedtest():
    settings = DashboardSettings.query.first()
    SPEEDTEST_COOLDOWN_IN_HOURS = settings.speedtest_cooldown
    NUMBER_OF_SPEEDTESTS = settings.number_of_speedtests
    n_hour_ago = datetime.datetime.now() - datetime.timedelta(
        hours=SPEEDTEST_COOLDOWN_IN_HOURS
    )
    recent_results = SpeedTestResult.query.filter(
        SpeedTestResult.timestamp > n_hour_ago
    ).all()

    if len(recent_results) < NUMBER_OF_SPEEDTESTS:
        speedtest_result = run_speedtest()
        if speedtest_result["status"] == "Error":
            return render_template(
                "error/speedtest_error.html", error=speedtest_result["message"]
            )

        if speedtest_result:
            new_result = SpeedTestResult(
                download_speed=speedtest_result["download_speed"],
                upload_speed=speedtest_result["upload_speed"],
                ping=speedtest_result["ping"],
            )
            db.session.add(new_result)
            db.session.commit()
            receiver_email = current_user.email
            subject = "Speedtest Result"
            context = {"speedtest_result": speedtest_result}
            body = render_template_from_file("src/templates/email_templates/speedtest_result.html", **context)
            send_email(receiver_email, subject, body, is_html=True)
            return render_template(
                "speedtest_result.html",
                speedtest_result=speedtest_result,
                source="Actual Test",
            )
    else:
        latest_result = recent_results[-1]
        next_test_time = latest_result.timestamp + datetime.timedelta(
            hours=SPEEDTEST_COOLDOWN_IN_HOURS
        )
        remaining_time_for_next_test = round(
            (next_test_time - datetime.datetime.now()).total_seconds() / 60
        )
        return render_template(
            "speedtest_result.html",
            speedtest_result=latest_result,
            source="Database",
            next_test_time=next_test_time,
            remaining_time_for_next_test=remaining_time_for_next_test,
        )



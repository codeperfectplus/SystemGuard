from flask import render_template, request, flash, blueprints

from src.config import app, db
from src.models import DashboardSettings

settings_bp = blueprints.Blueprint("settings", __name__)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    # Fetch the settings from the database and update them
    settings = DashboardSettings.query.first()
    if settings:
        if request.method == "POST":
            settings.speedtest_cooldown = int(request.form["speedtest_cooldown"])
            settings.number_of_speedtests = int(request.form["number_of_speedtests"])
            settings.timezone = request.form["timezone"]
            db.session.commit()
            flash("Settings updated successfully!", "success")
        return render_template("settings.html", settings=settings)


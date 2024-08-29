import psutil

from flask import render_template, blueprints

from src.config import app

disk_usage_bp = blueprints.Blueprint("disk_usage", __name__)

@app.route("/disk_usage")
def disk_usage():
    disk_info = {
        "disk_usage": psutil.disk_usage("/").percent,
        "disk_total": round(psutil.disk_usage("/").total / (1024**3), 2),  # In GB
        "disk_used": round(psutil.disk_usage("/").used / (1024**3), 2),  # In GB
        "disk_free": round(psutil.disk_usage("/").free / (1024**3), 2),  # In GB
    }
    return render_template("disk_usage.html", disk_info=disk_info)


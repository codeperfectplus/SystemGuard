import psutil

from flask import render_template, blueprints

from src.config import app
from src.utils import get_cached_value, get_disk_free, get_disk_total, get_disk_used, get_disk_usage_percent

disk_info_bp = blueprints.Blueprint("disk_usage", __name__)

@app.route("/disk_usage")
def disk_usage():
    disk_total = get_cached_value("disk_total", get_disk_total)
    system_info = {
        "disk_usage": get_disk_usage_percent(),
        "disk_total": disk_total,
        "disk_used": get_disk_used(),
        "disk_free": get_disk_free(),
    }
    return render_template("disk_info.html", system_info=system_info)


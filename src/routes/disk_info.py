import psutil

from flask import render_template, blueprints, flash

from src.config import app
from src.utils import get_cached_value, get_disk_free, get_disk_total, get_disk_used, get_disk_usage_percent
from src.models import DashboardSettings

disk_info_bp = blueprints.Blueprint("disk_usage", __name__)

@app.route("/disk_usage")
def disk_usage():
    settings = DashboardSettings.query.first()
    if not settings.is_disk_info_enabled:
        flash("You do not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")
    disk_total = get_cached_value("disk_total", get_disk_total)
    system_info = {
        "disk_usage": get_disk_usage_percent(),
        "disk_total": disk_total,
        "disk_used": get_disk_used(),
        "disk_free": get_disk_free(),
    }
    return render_template("info_pages/disk_info.html", system_info=system_info)


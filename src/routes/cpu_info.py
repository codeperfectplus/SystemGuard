import psutil
from flask import render_template, blueprints, flash

from flask_login import login_required

from src.config import app
from src.utils import get_cpu_core_count, get_cpu_frequency, cpu_usage_percent, get_cpu_temp, get_cached_value
from src.models import PageToggleSettings, SystemInformation

cpu_info_bp = blueprints.Blueprint("cpu_usage", __name__)

@app.route("/cpu_usage")
@login_required
def cpu_usage():
    page_toggles_settings = PageToggleSettings.query.first()
    if not page_toggles_settings.is_cpu_info_enabled:
        flash("You do not have permission to view this page.", "danger")
        return render_template("error/403.html")
    
    current_temp, high_temp, critical_temp = get_cpu_temp()
    cpu_core = get_cached_value("cpu_core", get_cpu_core_count)
    system_info = {
        "cpu_core": cpu_core,
        "cpu_frequency": get_cpu_frequency(),
        "cpu_percent": cpu_usage_percent(),
        "current_temp": current_temp,
        "high_temp": high_temp,
        "critical_temp": critical_temp,
    }

    recent_system_info_entries = SystemInformation.query.all()
    if recent_system_info_entries:
        # Extract cpu_percent and timestamp from the query results
        cpu_data = [info.cpu_percent for info in recent_system_info_entries]
        time_data = [info.timestamp for info in recent_system_info_entries]

        print("CPU Data:", cpu_data)
        print("Time Data:", time_data)
    return render_template("info_pages/cpu_info.html", system_info=system_info,
                            cpu=cpu_data, time=time_data)
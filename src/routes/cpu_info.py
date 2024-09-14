from flask import render_template, blueprints

from flask_login import login_required

from src.config import app
from src.utils import get_cpu_core_count, get_cpu_frequency, cpu_usage_percent, get_cpu_temp, get_cached_value
from src.routes.helper.common_helper import check_page_toggle
cpu_info_bp = blueprints.Blueprint("cpu_usage", __name__)

@app.route("/cpu_usage")
@login_required
@check_page_toggle("is_cpu_info_enabled")
def cpu_usage():
    
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

    return render_template("info_pages/cpu_info.html", system_info=system_info)

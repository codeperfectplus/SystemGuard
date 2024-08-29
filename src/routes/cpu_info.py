import psutil
from flask import render_template, blueprints

from src.config import app
from src.utils import get_cpu_core_count, get_cpu_frequency, cpu_usage_percent, get_cpu_temp

cpu_info_bp = blueprints.Blueprint("cpu_usage", __name__)

@app.route("/cpu_usage")
def cpu_usage():
    current_temp, high_temp, critical_temp = get_cpu_temp()
    cpu_data = {
        "cpu_core": get_cpu_core_count(),
        "cpu_frequency": get_cpu_frequency(),
        "cpu_usage_percent": cpu_usage_percent(),
        "current_temp": current_temp,
        "high_temp": high_temp,
        "critical_temp": critical_temp,
    }
    return render_template("cpu_info.html", cpu_data=cpu_data)
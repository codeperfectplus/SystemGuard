import psutil
from flask import render_template, blueprints

from src.config import app
from src.utils import get_cached_value, get_memory_percent, get_memory_available, get_memory_used, get_swap_memory_info
from src.models import DashboardSettings

memory_info_bp = blueprints.Blueprint("memory_usage", __name__)


@app.route("/memory_usage")
def memory_usage():
    settings = DashboardSettings.query.first()
    if not settings.is_memory_info_enabled:
        return render_template("error/404.html")
    memory_available = get_cached_value("memory_available", get_memory_available) 
    system_info = {
        "memory_percent": get_memory_percent(),
        "memory_available": memory_available,
        "memory_used": get_memory_used(),
    }

    swap_info = get_swap_memory_info()
    system_info.update(swap_info)

    return render_template("memory_info.html", system_info=system_info)

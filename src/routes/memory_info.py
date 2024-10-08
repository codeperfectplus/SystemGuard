from flask import render_template, blueprints
from flask_login import login_required

from src.config import app
from src.utils import get_cached_value, get_memory_percent, get_memory_available, get_memory_used, get_swap_memory_info, get_flask_memory_usage
from src.routes.helper.common_helper import check_page_toggle

memory_info_bp = blueprints.Blueprint("memory_usage", __name__)


@app.route("/memory_usage")
@login_required
@check_page_toggle("is_memory_info_enabled")
def memory_usage():
    memory_available = get_cached_value("memory_available", get_memory_available) 
    system_info = {
        "memory_percent": get_memory_percent(),
        "memory_available": memory_available,
        "memory_used": get_memory_used(),
        'dashboard_memory_usage': get_flask_memory_usage(),
    }

    swap_info = get_swap_memory_info()
    system_info.update(swap_info)

    return render_template("info_pages/memory_info.html", system_info=system_info)

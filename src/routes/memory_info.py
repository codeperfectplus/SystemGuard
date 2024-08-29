import psutil
from flask import render_template, blueprints

from src.utils import swap_memory_info

from src.config import app

memory_info_bp = blueprints.Blueprint("memory_usage", __name__)

@app.route("/memory_usage")
def memory_usage():
    total_swap, used_swap, free_swap = swap_memory_info()
    system_info = {
        "memory_percent": psutil.virtual_memory().percent,
        "memory_available": round(
            psutil.virtual_memory().available / (1024**3), 2
        ),  # In GB
        "memory_used": round(psutil.virtual_memory().used / (1024**3), 2),  # In GB,
        "total_swap": round(total_swap / (1024**3), 2),  # In GB
        "used_swap": round(used_swap / (1024**3), 2),  # In GB
        "free_swap": round(free_swap / (1024**3), 2),  # In GB
    }
    return render_template("memory_info.html", system_info=system_info)

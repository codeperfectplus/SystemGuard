import psutil
from flask import render_template, blueprints

from src.config import app

memory_usage_bp = blueprints.Blueprint("memory_usage", __name__)

@app.route("/memory_usage")
def memory_usage():
    memory_info = {
        "memory_percent": psutil.virtual_memory().percent,
        "memory_available": round(
            psutil.virtual_memory().available / (1024**3), 2
        ),  # In GB
        "memory_used": round(psutil.virtual_memory().used / (1024**3), 2),  # In GB
    }
    return render_template("memory_usage.html", memory_info=memory_info)

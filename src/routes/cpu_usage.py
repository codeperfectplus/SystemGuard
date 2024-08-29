import psutil
from flask import render_template, blueprints

from src.config import app

cpu_usage_bp = blueprints.Blueprint("cpu_usage", __name__)

@app.route("/cpu_usage")
def cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    return render_template("cpu_usage.html", cpu_usage=cpu_usage)
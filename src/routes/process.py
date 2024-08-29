from flask import request, render_template, blueprints

from src.config import app
from src.utils import get_top_processes

process_bp = blueprints.Blueprint("process", __name__)


@app.route("/process", methods=["GET", "POST"])
def process():
    number_of_processes = 5  # Default number
    if request.method == "POST":
        number_of_processes = int(request.form.get("number", 5))
    
    top_processes = get_top_processes(number_of_processes)
    return render_template("process.html", processes=top_processes, number=number_of_processes)
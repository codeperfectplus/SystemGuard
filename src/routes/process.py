import os
from flask import request, render_template, blueprints, redirect, url_for, flash

from src.config import app
from src.utils import get_top_processes

process_bp = blueprints.Blueprint("process", __name__)

@app.route("/process", methods=["GET", "POST"])
def process():
    number_of_processes = 5  # Default number

    if request.method == "POST":
        if "kill_pid" in request.form:
            # Handle killing the process
            pid_to_kill = request.form.get("kill_pid")
            process_name = request.form.get("process_name")
            try:
                os.kill(int(pid_to_kill), 9)  # Sends a SIGKILL signal
                flash(f"Process '{process_name}' (PID {pid_to_kill}) killed successfully.", "success")
            except Exception as e:
                flash(f"Failed to kill process '{process_name}' (PID {pid_to_kill}). Error: {e}", "danger")
            return redirect(url_for("process"))  # Refresh the page after killing process

        # Handle the number of processes to display
        number_of_processes = int(request.form.get("number", 5))

    top_processes = get_top_processes(number_of_processes)
    return render_template("process.html", processes=top_processes, number=number_of_processes)

import os
import subprocess
from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    blueprints,
    session,
)
from flask_login import current_user
from src.config import app
from src.utils import get_top_processes, render_template_from_file, ROOT_DIR
from src.alerts import send_smtp_email
from src.config import get_app_info
from src.routes.helper.common_helper import (
    admin_required, 
    check_page_toggle, 
    handle_sudo_password)

process_bp = blueprints.Blueprint("process", __name__)

@app.route("/process", methods=["GET", "POST"])
@check_page_toggle("is_process_info_enabled")
@admin_required
@handle_sudo_password("process")
def process():
    # Retrieve number of processes from session or set default
    number_of_processes = session.get("number_of_processes", 50)
    sort_by = request.args.get("sort", "cpu")  # Default to sort by CPU usage
    order = request.args.get("order", "asc")  # Default to ascending order
    toggle_order = "desc" if order == "asc" else "asc"  # Toggle order for next click
        
    sudo_password = session.get("sudo_password", "")
    if "kill_pid" in request.form:
        pid_to_kill = request.form.get("kill_pid")
        process_name = request.form.get("process_name")
        try:
            # Kill process with sudo
            result = subprocess.run(
                ['sudo', '-S', 'kill', '-9', str(pid_to_kill)],
                input=sudo_password + '\n',  # Pass the sudo password
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )

            if result.returncode == 0:
                flash(
                    f"Process '{process_name}' (PID {pid_to_kill}) killed successfully.",
                    "success",
                )
                receiver_email = current_user.email
                subject = (
                    f"Process '{process_name}' (PID {pid_to_kill}) killed successfully."
                )
                context = {
                    "process_name": process_name,
                    "pid_to_kill": pid_to_kill,
                    "username": current_user.username,
                    "title": get_app_info()["title"],
                }
                process_killed_template = os.path.join(
                    ROOT_DIR, "src/templates/email_templates/process_killed.html"
                )
                email_body = render_template_from_file(
                    process_killed_template, **context
                )
                send_smtp_email(receiver_email, subject, email_body, is_html=True)
            else:
                flash(
                    f"Failed to kill process '{process_name}' (PID {pid_to_kill}). Error: {result.stderr}",
                    "danger",
                )
        except Exception as e:
            flash(
                f"Failed to kill process '{process_name}' (PID {pid_to_kill}). Error: {e}",
                "danger",
            )
        return redirect(
            url_for("process")
        )  # Refresh the page after killing process

    # Handle the number of processes to display
    number_of_processes = int(request.form.get("number", 50))
    session["number_of_processes"] = (
        number_of_processes  # Store the number in session
    )

    # Retrieve processes
    top_processes = get_top_processes(number_of_processes)

    # Sorting logic based on selected criteria
    if sort_by == "cpu":
        top_processes.sort(key=lambda x: x[1], reverse=(order == "desc"))
    elif sort_by == "memory":
        top_processes.sort(key=lambda x: x[2], reverse=(order == "desc"))
    elif sort_by == "name":
        top_processes.sort(key=lambda x: x[0], reverse=(order == "desc"))

    return render_template(
        "info_pages/process.html",
        processes=top_processes,
        number=number_of_processes,
        toggle_order=toggle_order,
    )

import os
from flask import request, render_template, redirect, url_for, flash, session, blueprints
from flask_login import login_required, current_user
from src.config import app
from src.utils import get_top_processes, render_template_from_file, ROOT_DIR
from src.models import  FeatureToggleSettings
from src.scripts.email_me import send_smpt_email

process_bp = blueprints.Blueprint("process", __name__)

@app.route("/process", methods=["GET", "POST"])
@login_required
def process():
    feature_toggles_settings = FeatureToggleSettings.query.first()
    if not feature_toggles_settings.is_process_info_enabled:
        flash("You do not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")
    if current_user.user_level != "admin":
        flash("You do not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")

    # Retrieve number of processes from session or set default
    number_of_processes = session.get('number_of_processes', 50)
    sort_by = request.args.get('sort', 'cpu')  # Default to sort by CPU usage
    order = request.args.get('order', 'asc')  # Default to ascending order
    toggle_order = 'desc' if order == 'asc' else 'asc'  # Toggle order for next click

    if request.method == "POST":
        if "kill_pid" in request.form:
            pid_to_kill = request.form.get("kill_pid")
            process_name = request.form.get("process_name")
            try:
                os.kill(int(pid_to_kill), 9)  # Sends a SIGKILL signal
                flash(f"Process '{process_name}' (PID {pid_to_kill}) killed successfully.", "success")
                receiver_email = current_user.email
                subject = f"Process '{process_name}' (PID {pid_to_kill}) killed successfully."
                context = {"process_name": process_name, "pid_to_kill": pid_to_kill, "username": current_user.username}
                process_killed_template = os.path.join(ROOT_DIR, "src/templates/email_templates/process_killed.html")
                html_body = render_template_from_file(process_killed_template, **context)
                send_smpt_email(receiver_email, subject, html_body, is_html=True)
            except Exception as e:
                flash(f"Failed to kill process '{process_name}' (PID {pid_to_kill}). Error: {e}", "danger")
            return redirect(url_for("process"))  # Refresh the page after killing process

        # Handle the number of processes to display
        number_of_processes = int(request.form.get("number", 50))
        session['number_of_processes'] = number_of_processes  # Store the number in session

    # Retrieve processes
    top_processes = get_top_processes(number_of_processes)

    # Sorting logic based on selected criteria
    if sort_by == 'cpu':
        top_processes.sort(key=lambda x: x[1], reverse=(order == 'desc'))
    elif sort_by == 'memory':
        top_processes.sort(key=lambda x: x[2], reverse=(order == 'desc'))
    elif sort_by == 'name':
        top_processes.sort(key=lambda x: x[0], reverse=(order == 'desc'))

    return render_template("info_pages/process.html", processes=top_processes, number=number_of_processes, toggle_order=toggle_order)

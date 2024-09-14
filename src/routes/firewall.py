from flask import Blueprint, render_template, request, session, flash

from src.config import app
from src.routes.helper.firewall_helper import (
    list_open_ports,
    enable_port, 
    disable_port)
from src.routes.helper.common_helper import admin_required, handle_sudo_password
from flask import request, session, flash

firewall_bp = Blueprint('firewall', __name__)

@app.route('/firewall', methods=['GET', 'POST'])
@admin_required
@handle_sudo_password("firewall")
def firewall():
    """
    Flask view for the firewall page. Handles both GET and POST requests:
    - GET: Displays the open ports and checks if sudo password is saved in session.
    - POST: Handles sudo password verification, enabling/disabling ports, and
      session management.

    :return: Rendered firewall.html page with the appropriate data and message.
    """
    message = ''
    open_ports = []

    if request.method == 'POST':
        if 'port' in request.form and 'protocol' in request.form and 'action' in request.form:
            port = request.form['port']
            protocol = request.form['protocol']
            action = request.form['action']
            session['protocol'] = protocol
            session['action'] = action
            
            # Handle port enabling/disabling based on the action
            if action == 'Enable':
                message = enable_port(port, protocol, sudo_password)
            elif action == 'Disable':
                message = disable_port(port, protocol, sudo_password)
            
            flash(message, 'info')
            
            # List the current open ports
            open_ports, error_message = list_open_ports(sudo_password)
            if error_message:
                message = error_message
                flash(message, 'danger')
        else:
            open_ports, error_message = list_open_ports(sudo_password)
            flash("Showing open ports.", 'info')
            if error_message:
                message = error_message
                flash(message, 'danger')
    else:
        sudo_password = session.get('sudo_password', '')
        if sudo_password:
            open_ports, error_message = list_open_ports(sudo_password)
            if error_message:
                message = error_message
                flash(message, 'danger')
        else:
            message = "Please enter your sudo password to view the open ports."
            flash(message, 'info')

    return render_template('firewall/firewall.html', message=message, open_ports=open_ports)

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import subprocess

from src.config import app
firewall_bp = Blueprint('firewall', __name__)

def reset_sudo_timestamp():
    """
    Reset the sudo timestamp, which requires the user to input their sudo password again
    the next time a sudo command is executed.
    """
    subprocess.run(['sudo', '-k'])

def check_sudo_password(sudo_password):
    """
    Verify the given sudo password by executing a harmless sudo command.
    If the password is correct, it returns True. Otherwise, returns False.

    :param sudo_password: The user's sudo password to validate.
    :return: True if the password is correct, otherwise False.
    """
    try:
        # Test if the sudo password is valid by running a safe sudo command
        result = subprocess.run(
            ['sudo', '-S', 'true'],
            input=f'{sudo_password}\n',
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    
    except Exception as e:
        # Log any exception that occurs while validating the sudo password
        return False, str(e)

def list_open_ports(sudo_password):
    """
    List all open TCP and UDP ports using iptables.

    :param sudo_password: The sudo password used to run the iptables command.
    :return: A list of open ports and an error message if applicable.
    """
    try:
        # Use iptables to list all open ports
        result = subprocess.run(['sudo', '-S', 'iptables', '-L', '-n'], input=f"{sudo_password}\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if "incorrect password" in result.stderr:
            return [], "Incorrect sudo password. Please try again."
        
        open_ports = []
        # Parse output and extract open TCP/UDP ports
        for line in output.splitlines():
            if "ACCEPT" in line:
                if 'tcp' in line:
                    open_ports.append(('TCP', line))
                elif 'udp' in line:
                    open_ports.append(('UDP', line))
        return open_ports, ""
    
    except Exception as e:
        # Handle and return any exception that occurs while listing ports
        return [], str(e)

def enable_port(port, protocol, sudo_password):
    """
    Enable a specified port for a given protocol by adding an iptables rule.

    :param port: The port number to enable.
    :param protocol: The protocol (TCP/UDP) for the port.
    :param sudo_password: The sudo password required to execute the iptables command.
    :return: A success message if the port is enabled, otherwise an error message.
    """
    try:
        # Build the iptables command to enable a port
        command = ['sudo', '-S', 'iptables', '-A', 'INPUT', '-p', protocol, '--dport', str(port), '-j', 'ACCEPT']
        result = subprocess.run(command, input=f'{sudo_password}\n', text=True)
        if result.returncode == 0:
            return f"Port {port} with protocol {protocol} enabled."
        else:
            return result.stderr
    except Exception as e:
        # Handle and return any exception that occurs while enabling the port
        return str(e)

def disable_port(port, protocol, sudo_password):
    """
    Disable a specified port for a given protocol by removing the iptables rule.

    :param port: The port number to disable.
    :param protocol: The protocol (TCP/UDP) for the port.
    :param sudo_password: The sudo password required to execute the iptables command.
    :return: A success message if the port is disabled, otherwise an error message.
    """
    try:
        # Build the iptables command to disable a port
        command = ['sudo', '-S', 'iptables', '-D', 'INPUT', '-p', protocol, '--dport', str(port), '-j', 'ACCEPT']
        result = subprocess.run(command, input=f'{sudo_password}\n', text=True)
        if result.returncode == 0:
            return f"Port {port} with protocol {protocol} disabled."
        else:
            return result.stderr
    except Exception as e:
        # Handle and return any exception that occurs while disabling the port
        return str(e)

@app.route('/firewall', methods=['GET', 'POST'])
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

        # Clear session and reset sudo timestamp
        if 'clear_session' in request.form:
            session.pop('sudo_password', None)
            session.pop('protocol', None)
            session.pop('action', None)
            reset_sudo_timestamp()
            return redirect(url_for('firewall'))

        # Validate sudo password and store it in the session
        if 'sudo_password' in request.form:
            sudo_password = request.form['sudo_password']
            if not check_sudo_password(sudo_password):
                message = "Incorrect sudo password. Please try again."
                flash(message, 'danger')
                return render_template('firewall.html', message=message, open_ports=open_ports)
            session['sudo_password'] = sudo_password
            flash("Sudo password saved in session successfully.", 'info')
        else:
            sudo_password = session.get('sudo_password', '')

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

    return render_template('firewall.html', message=message, open_ports=open_ports)

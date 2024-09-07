from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import subprocess

from src.config import app
firewall_bp = Blueprint('firewall', __name__)

def reset_sudo_timestamp():
    subprocess.run(['sudo', '-k'])

def check_sudo_password(sudo_password):
    try:
        # Run a harmless sudo command to check the password
        result = subprocess.run(
            ['sudo', '-S', 'true'],
            input=f'{sudo_password}\n',
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Check if the command was successful
        if result.returncode == 0:
            return True
        else:
            return False
    
    except Exception as e:
        return False, str(e)
    
def list_open_ports(sudo_password):
    try:
        result = subprocess.run(['sudo', '-S', 'iptables', '-L', '-n'], input=f"{sudo_password}\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if "incorrect password" in result.stderr:
            return [], "Incorrect sudo password. Please try again."
        open_ports = []
        for line in output.splitlines():
            if "ACCEPT" in line:
                if 'tcp' in line:
                    open_ports.append(('TCP', line))
                elif 'udp' in line:
                    open_ports.append(('UDP', line))
        return open_ports, ""
    except Exception as e:
        return [], str(e)

def enable_port(port, protocol, sudo_password):
    try:
        sudo_password = session.get('sudo_password', '')
        print("sudo_password", sudo_password)
        command = ['sudo', '-S', 'iptables', '-A', 'INPUT', '-p', protocol, '--dport', str(port), '-j', 'ACCEPT']
        result = subprocess.run(command, input=f'{sudo_password}\n', text=True)
        if result.returncode == 0:
            return f"Port {port} with protocol {protocol} enabled."
        else:
            return result.stderr
    except Exception as e:
        return str(e)

def disable_port(port, protocol, sudo_password):
    try:
        command = ['sudo', '-S', 'iptables', '-D', 'INPUT', '-p', protocol, '--dport', str(port), '-j', 'ACCEPT']
        result = subprocess.run(command, input=f'{sudo_password}\n', text=True)
        if result.returncode == 0:
            return f"Port {port} with protocol {protocol} disabled."
        else:
            return result.stderr
    except Exception as e:
        return str(e)

@app.route('/firewall', methods=['GET', 'POST'])
def firewall():
    message = ''
    open_ports = []

    if request.method == 'POST':

        # logic to clear the session and sudo password from the session and reset the sudo timestamp
        if 'clear_session' in request.form:
            session.pop('sudo_password', None)
            session.pop('protocol', None)
            session.pop('action', None)
            reset_sudo_timestamp()

            return redirect(url_for('firewall'))

        # logic to check if the sudo password is correct and store it in the session
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
            
            if action == 'Enable':
                message = enable_port(port, protocol, sudo_password)
            elif action == 'Disable':
                message = disable_port(port, protocol, sudo_password)
            
            flash(message, 'info')
            
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
        print("sudo_password", sudo_password)
        if sudo_password:
            open_ports, error_message = list_open_ports(sudo_password)
            if error_message:
                message = error_message
                flash(message, 'danger')
        else:
            message = "Please enter your sudo password to view the open ports."
            flash(message, 'info')

    return render_template('firewall.html', message=message, open_ports=open_ports)


import subprocess

def reset_sudo_timestamp():
    """
    Reset the sudo timestamp, which requires the user to input their sudo password again
    the next time a sudo command is executed.
    """
    subprocess.run(['sudo', '-k'])

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


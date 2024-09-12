import os
import subprocess

def get_system_node_name():
    """ 
    Get the system node name.
    ---
    Parameters:
    ---
    Returns:
        str: System node name
    """
    return os.uname().nodename

def get_ip_address():
    try:
        # Run the command `hostname -I` to get the IP addresses
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True)
        
        # Split the output by spaces and get the first IP address
        ip_address = result.stdout.split()[0]
        
        return ip_address
    except (IndexError, subprocess.CalledProcessError) as e:
        print(f"Error occurred: {e}")
        return None
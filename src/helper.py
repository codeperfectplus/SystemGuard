import os
import subprocess

def get_system_username():
    """
    Get the current system username.
    ---
    Parameters:
    ---
    Returns:
        str: System username.
    """
    return os.getlogin()

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
    

def check_installation_information():
    # check if .git exists, if not, return False
    # when .git exists, return True and which branch is checked out

    # check if .git exists
    output = {
        "is_git_repo": False,
        "git_branch": None,
        "git_commit": None,
        "git_repo": None,
    }
    if not os.path.exists(".git"):
        return output
    
    # read the HEAD file    
    with open(".git/HEAD", "r") as f:
        head = f.read().strip()

    # check if HEAD is a branch
    if head.startswith("ref: refs/heads/"):
        branch = head.replace("ref: refs/heads/", "")
        output["is_git_repo"] = True
        output["git_branch"] = branch
    
    return output

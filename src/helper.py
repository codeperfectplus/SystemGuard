import os
import subprocess
from dotenv import load_dotenv

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
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True)
        ip_address = result.stdout.split()[0]
        return ip_address
    except (IndexError, subprocess.CalledProcessError) as e:
        return None

def check_installation_information():
    # Output dictionary to store results
    output = {
        "is_git_repo": False,
        "git_branch": None,
        "git_commit": None,
        "git_repo": None,
        "last_commit_date": None,
        "last_commit_message": None,
        "update_available": False
    }

    # Check if .git directory exists
    if not os.path.isdir(".git"):
        return output

    # Read the HEAD file to get the current branch
    try:
        with open(".git/HEAD", "r") as f:
            head = f.read().strip()
    except IOError:
        return output

    # Check if HEAD is a branch
    if head.startswith("ref: refs/heads/"):
        branch = head.replace("ref: refs/heads/", "")
        output["is_git_repo"] = True
        output["git_branch"] = branch

    # Get the last commit information
    try:
        result = subprocess.run(["git", "log", "-1", "--pretty=format:%H|%ad|%s", "--date=short"], capture_output=True, text=True, check=True)
        commit_data = result.stdout.split("|")
        output["git_commit"] = commit_data[0]
        output["last_commit_date"] = commit_data[1]
        output["last_commit_message"] = commit_data[2]
    except subprocess.CalledProcessError:
        pass

    # Check for updates
    try:
        result = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True, check=True)
        if "Your branch is up to date" in result.stdout:
            output["update_available"] = False
        else:
            output["update_available"] = True
    except subprocess.CalledProcessError:
        pass

    return output



def load_secret_key():
    """Load the secret key for the application."""
    load_dotenv()
    secret_key = os.getenv('SYSTEMGUARD_KEY')    
    if secret_key:
        return secret_key
    else:
        try:
            with open('secret.key', 'rb') as key_file:
                secret_key = key_file.read()
                return secret_key
        except FileNotFoundError:
            raise FileNotFoundError("The secret key file 'secret.key' was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the secret key: {e}")

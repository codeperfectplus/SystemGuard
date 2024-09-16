#!/bin/bash

# if run with sudo, exit
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a non-root user."
    exit 1
fi

# Function to log messages with timestamps
log_message() {
    # Check if the level is passed; if not, set it to "INFO" as default.
    local level="${1:-INFO}"
    local message

    # Check if a second argument exists, indicating that the first is the level.
    if [ -z "$2" ]; then
        message="$1" # Only message is passed, assign the first argument to message.
        level="INFO" # Default level when only message is passed.
    else
        message="$2" # When both level and message are passed.
    fi

    # Define colors based on log levels.
    local color_reset="\033[0m"
    local color_debug="\033[1;34m"    # Blue
    local color_info="\033[1;32m"     # Green
    local color_warning="\033[1;33m"  # Yellow
    local color_error="\033[1;31m"    # Red
    local color_critical="\033[1;41m" # Red background

    # Select color based on level.
    local color="$color_reset"
    case "$level" in
    DEBUG)
        color="$color_debug"
        ;;
    INFO)
        color="$color_info"
        ;;
    WARNING)
        color="$color_warning"
        ;;
    ERROR)
        color="$color_error"
        ;;
    CRITICAL)
        color="$color_critical"
        ;;
    *)
        color="$color_reset" # Default to no color if the level is unrecognized.
        ;;
    esac

    # Log the message with timestamp, level, and message content, applying the selected color.
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') ${color}[$level]${color_reset} - $message" | tee -a "$LOG_FILE"
}

# Determine the directory where this script is located
SCRIPT_DIR="$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0")")"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
FLASK_APP_PATH="${FLASK_APP_PATH:-$PROJECT_DIR/app.py}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$PROJECT_DIR/requirements.txt}"
SCRIPT_TO_CHECK_REQUIREMENTS="$SCRIPT_DIR/missing_dependcy.py"
FLASK_PORT="${FLASK_PORT:-5050}"
APP_NAME="systemguard"
LOG_FILE="/home/$(whoami)/logs/flask.log"
USERNAME="$(whoami)"
CONDA_ENV_NAME=$APP_NAME
GIT_REMOTE_URL="https://github.com/codeperfectplus/SystemDashboard" # Set this if you want to add a remote
ENV_FILE="/home/$(whoami)/.bashrc"

# Export Flask environment variables
export FLASK_APP="$FLASK_APP_PATH"
export FLASK_ENV=production
export FLASK_RUN_PORT="$FLASK_PORT"
export FLASK_RUN_HOST="0.0.0.0"



# Function to fetch the value of an environment variable from a file
fetch_env_variable() {
    var_name=$1 # The name of the environment variable to fetch
    # Check if the environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        echo "Error: Environment file '$ENV_FILE' not found."
        return 1
    fi

    # Fetch the value of the environment variable
    var_value=$(grep -E "^${var_name}=" "$ENV_FILE" | sed -E "s/^${var_name}=(.*)/\1/")

    # Check if the variable was found and has a value
    if [ -z "$var_value" ]; then
        echo "Error: Variable '$var_name' not found in '$ENV_FILE'."
        return 1
    fi

    # Print the value of the environment variable
    echo "$var_value"
}

auto_update=$(fetch_env_variable "sg_auto_update")
# Fetch from bashrc for auto-update
echo "Auto update for $APP_NAME is set to $auto_update"

# Ensure log directory exists
LOG_DIR="$(dirname "$LOG_FILE")"
mkdir -p "$LOG_DIR"

# Check for Miniconda3 and Anaconda3
CONDA_PATHS=("/home/$USERNAME/miniconda3" "/home/$USERNAME/anaconda3")
CONDA_FOUND=false

for CONDA_PATH in "${CONDA_PATHS[@]}"; do
    if [ -d "$CONDA_PATH" ]; then
        CONDA_FOUND=true
        CONDA_EXECUTABLE="$CONDA_PATH/bin/conda"
        CONDA_SETUP_SCRIPT="$CONDA_PATH/etc/profile.d/conda.sh"
        source "$CONDA_SETUP_SCRIPT" &>/dev/null
        break
    fi
done

if [ "$CONDA_FOUND" = false ]; then
    log_message "Neither Miniconda3 nor Anaconda3 found. Ensure Conda is installed."
    exit 1
fi

# Check if Conda setup script exists
if [ ! -f "$CONDA_SETUP_SCRIPT" ]; then
    log_message "Conda setup script not found at $CONDA_SETUP_SCRIPT."
    exit 1
fi

# Check if the Conda environment exists and create it if not
if ! conda info --envs | awk '{print $1}' | grep -q "^$CONDA_ENV_NAME$"; then
    log_message "Conda environment '$CONDA_ENV_NAME' not found. Creating it..."
    conda create -n "$CONDA_ENV_NAME" python=3.10 -y

    log_message "Activating Conda environment '$CONDA_ENV_NAME' and installing requirements."
    conda run -n "$CONDA_ENV_NAME" pip install -r "$REQUIREMENTS_FILE"
else
    log_message "Activating existing Conda environment '$CONDA_ENV_NAME'."
fi

fetch_latest_changes() {
    local project_dir="$1"
    local git_remote_url="${2-}" # Optional remote URL if needed

    # Check if the project directory is set and exists
    if [[ -z "$project_dir" || ! -d "$project_dir" ]]; then
        log_message "ERROR" "Invalid project directory specified."
        return 1
    fi

    # Check if Git is installed
    if ! command -v git &>/dev/null; then
        log_message "ERROR" "Git is not installed. Please install Git and try again."
        return 1
    fi

    # Check if the directory is a Git repository
    if [ -d "$project_dir/.git" ]; then
        log_message "INFO" "Repository found at $project_dir. Checking the current branch and for latest changes..."

        # Navigate to the project directory
        pushd "$project_dir" >/dev/null

        # Get the current branch name
        branch=$(git symbolic-ref --short HEAD 2>/dev/null)
        log_message "INFO" "Current branch is '$branch'."

        # Check if there are untracked files
        if git status --porcelain | grep '^[?]'; then
            # Check if the repository has any commits
            if [ $(git rev-list --count HEAD 2>/dev/null) -gt 0 ]; then
                # Repository has commits, proceed with stashing
                log_message "INFO" "Stashing untracked files..."
                if git stash -u; then
                    log_message "INFO" "Untracked files stashed successfully."
                    stash_applied=true
                else
                    log_message "ERROR" "Failed to stash untracked files."
                    popd >/dev/null
                    return 1
                fi
            else
                log_message "ERROR" "Repository does not have any commits. Cannot stash untracked files."
                log_message "INFO" "Manual intervention required to handle untracked files."
                popd >/dev/null
                return 1
            fi
        fi

        if git pull origin "$branch"; then
            log_message "INFO" "Successfully pulled the latest changes from branch '$branch'."
        else
            log_message "ERROR" "Failed to pull the latest changes. Check your network connection or repository settings."
            popd >/dev/null
            return 1
        fi

        # Apply stashed changes if any
        if [ "$stash_applied" = true ]; then
            log_message "INFO" "Applying stashed changes..."
            git stash pop
        fi

        # Return to the original directory
        popd >/dev/null
    fi
}

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=$FLASK_PORT" >/dev/null; then
    conda run -n "$CONDA_ENV_NAME" pip install -r "$REQUIREMENTS_FILE"
    log_message "INFO" "Flask app is not running. Checking repository and starting it..."
    [ "$auto_update" = true ] && fetch_latest_changes $PROJECT_DIR $GIT_REMOTE_URL

    log_message "INFO" "Starting Flask app..."
    # Ensure environment activation and `flask` command
    bash -c "source $CONDA_SETUP_SCRIPT && conda activate $CONDA_ENV_NAME && flask run --host=0.0.0.0 --port=$FLASK_PORT" &>>"$LOG_FILE" &
else
    log_message "INFO" "Flask app is already running."
fi

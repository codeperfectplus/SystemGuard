#!/bin/bash

# Function to log messages with timestamps
log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Determine the directory where this script is located
SCRIPT_DIR="$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0")")"

# Define variables for paths relative to the script's directory
FLASK_APP_PATH="${FLASK_APP_PATH:-$SCRIPT_DIR/app.py}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$SCRIPT_DIR/requirements.txt}"
FLASK_PORT="${FLASK_PORT:-5050}"
LOG_FILE="${SCRIPT_DIR}/my_script.log"
USERNAME="$(whoami)"

# Check for Miniconda3 and Anaconda3
CONDA_PATHS=("/home/$USERNAME/miniconda3" "/home/$USERNAME/anaconda3")
CONDA_FOUND=false

for CONDA_PATH in "${CONDA_PATHS[@]}"; do
    if [ -d "$CONDA_PATH" ]; then
        CONDA_FOUND=true
        break
    fi
done

if [ "$CONDA_FOUND" = false ]; then
    log_message "Neither Miniconda3 nor Anaconda3 found. Ensure Conda is installed."
    exit 1
fi

# Derive the path to the Conda setup script
CONDA_SETUP_SCRIPT="$CONDA_PATH/etc/profile.d/conda.sh"

# Check if Conda setup script exists
if [ ! -f "$CONDA_SETUP_SCRIPT" ]; then
    log_message "Conda setup script not found at $CONDA_SETUP_SCRIPT."
    exit 1
fi

# Initialize Conda
source "$CONDA_SETUP_SCRIPT"

# Define Conda environment name
CONDA_ENV_NAME="systemdashboard"

# Check if the Conda environment exists and create it if not
if ! conda env list | grep -q "$CONDA_ENV_NAME"; then
    log_message "Conda environment '$CONDA_ENV_NAME' not found. Creating it..."
    conda create -n "$CONDA_ENV_NAME" python=3.10 -y
    log_message "Activating Conda environment '$CONDA_ENV_NAME'."
    conda activate "$CONDA_ENV_NAME"
    log_message "Installing required packages."
    pip install -r "$REQUIREMENTS_FILE"
else
    log_message "Activating existing Conda environment '$CONDA_ENV_NAME'."
    conda activate "$CONDA_ENV_NAME"
fi

# Continue with the rest of your script
log_message "Conda environment '$CONDA_ENV_NAME' is active."

# Export Flask environment variables
export FLASK_APP="$FLASK_APP_PATH"
export FLASK_ENV=development  # or production

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=$FLASK_PORT" > /dev/null; then
    # git pull in FLASK_APP_PATH directory
    current_dir=$(pwd)
    cd "$SCRIPT_DIR"
    git stash && git pull
    cd "$current_dir"

    log_message "Starting Flask app..."
    flask run --host=0.0.0.0 --port="$FLASK_PORT" &
else
    log_message "Flask app is already running."
fi

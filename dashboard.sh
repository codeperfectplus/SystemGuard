#!/bin/bash

# Determine the directory where this script is located
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Define variables for paths relative to the script's directory
FLASK_APP_PATH="${FLASK_APP_PATH:-$SCRIPT_DIR/app.py}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$SCRIPT_DIR/requirements.txt}"
FLASK_PORT="${FLASK_PORT:-5050}"
LOG_FILE="${SCRIPT_DIR}/my_script.log"
USERNAME="$(whoami)"
CONDA_PATH="/home/$USERNAME/miniconda3"

# Find the Conda setup script dynamically
if [ -z "$CONDA_PATH" ]; then
    echo "Conda not found in PATH. Ensure Conda is installed and added to PATH." >> "$LOG_FILE"
    exit 1
fi

# Derive the path to the Conda setup script
CONDA_SETUP_SCRIPT="/home/$USERNAME/miniconda3/etc/profile.d/conda.sh"

# Check if Conda setup script exists
if [ ! -f "$CONDA_SETUP_SCRIPT" ]; then
    echo "Conda setup script not found at $CONDA_SETUP_SCRIPT" >> "$LOG_FILE"
    exit 1
fi

# Initialize Conda
source "$CONDA_SETUP_SCRIPT"

# Define Conda environment name
CONDA_ENV_NAME="systemdashboard"

# Check if the Conda environment exists and create it if not
if ! conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Conda environment '$CONDA_ENV_NAME' not found. Creating it..." >> "$LOG_FILE"
    conda create -n "$CONDA_ENV_NAME" python=3.10 -y
    echo "Activating Conda environment '$CONDA_ENV_NAME'" >> "$LOG_FILE"
    conda activate "$CONDA_ENV_NAME"
    echo "Installing required packages" >> "$LOG_FILE"
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Activating existing Conda environment '$CONDA_ENV_NAME'" >> "$LOG_FILE"
    conda activate "$CONDA_ENV_NAME"
fi

# Continue with the rest of your script
echo "Conda environment '$CONDA_ENV_NAME' is active." >> "$LOG_FILE"

# Export Flask environment variables
export FLASK_APP="$FLASK_APP_PATH"
export FLASK_ENV=development  # or production

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=$FLASK_PORT" > /dev/null; then
    # git pull on FLASK_APP_PATH directory
    current_dir=$(pwd)
    cd $SCRIPT_DIR
    git stash && git pull
    cd $current_dir

    echo "Starting Flask app..." >> "$LOG_FILE"
    flask run --host=0.0.0.0 --port="$FLASK_PORT" &
else
    echo "Flask app is already running." >> "$LOG_FILE"
fi

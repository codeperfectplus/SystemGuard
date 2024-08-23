#!/bin/bash

# Determine the directory where this script is located
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Define variables for paths relative to the script's directory
FLASK_APP_PATH="${FLASK_APP_PATH:-$SCRIPT_DIR/app.py}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$SCRIPT_DIR/requirements.txt}"
FLASK_PORT="${FLASK_PORT:-5050}"
LOG_FILE="${SCRIPT_DIR}/my_script.log"

# Full path to Conda setup script
CONDA_SETUP_SCRIPT="/home/deepak/miniconda3/etc/profile.d/conda.sh"

# Check if Conda setup script exists
if [ ! -f "$CONDA_SETUP_SCRIPT" ]; then
    echo "Conda setup script not found at $CONDA_SETUP_SCRIPT" >> "$LOG_FILE"
    exit 1
fi

# Initialize Conda
source "$CONDA_SETUP_SCRIPT"

# Activate the Conda environment
CONDA_ENV_NAME="systemdashboard"
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Activating Conda environment '$CONDA_ENV_NAME'" >> "$LOG_FILE"
    conda activate "$CONDA_ENV_NAME"
else
    echo "Conda environment '$CONDA_ENV_NAME' not found." >> "$LOG_FILE"
    exit 1
fi

# Continue with the rest of your script
echo "Conda environment '$CONDA_ENV_NAME' is active." >> "$LOG_FILE"

# Export Flask environment variables
export FLASK_APP="$FLASK_APP_PATH"
export FLASK_ENV=development  # or production

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=$FLASK_PORT" > /dev/null; then
    echo "Flask app is not running. Starting..." >> "$LOG_FILE"
    flask run --host=0.0.0.0 --port="$FLASK_PORT" &
else
    echo "Flask app is already running." >> "$LOG_FILE"
fi

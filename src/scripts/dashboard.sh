#!/bin/bash

# Function to log messages with timestamps
log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Determine the directory where this script is located
SCRIPT_DIR="$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0")")"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
FLASK_APP_PATH="${FLASK_APP_PATH:-$PROJECT_DIR/app.py}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-$PROJECT_DIR/requirements.txt}"
FLASK_PORT="${FLASK_PORT:-5050}"
LOG_FILE="/home/$(whoami)/logs/systemguard_flask.log"
USERNAME="$(whoami)"
CONDA_ENV_NAME="systemguard"

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

# Initialize Conda
source "$CONDA_SETUP_SCRIPT"

echo "Conda environment name: $CONDA_ENV_NAME"

# Check if the Conda environment exists and create it if not
if ! conda info --envs | awk '{print $1}' | grep -q "^$CONDA_ENV_NAME$"; then
    log_message "Conda environment '$CONDA_ENV_NAME' not found. Creating it..."
    conda create -n "$CONDA_ENV_NAME" python=3.10 -y

    log_message "Activating Conda environment '$CONDA_ENV_NAME' and installing requirements."
    conda run -n "$CONDA_ENV_NAME" pip install -r "$REQUIREMENTS_FILE"
else
    log_message "Activating existing Conda environment '$CONDA_ENV_NAME'."
fi

# Continue with the rest of your script
log_message "Conda environment '$CONDA_ENV_NAME' is active."

# Export Flask environment variables
export FLASK_APP="$FLASK_APP_PATH"
export FLASK_ENV=development  # or production

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=$FLASK_PORT" > /dev/null; then
    log_message "Flask app is not running. Checking repository and starting it..."

    log_message "Starting Flask app..."
    # Ensure environment activation and `flask` command
    bash -c "source $CONDA_SETUP_SCRIPT && conda activate $CONDA_ENV_NAME && flask run --host=0.0.0.0 --port=$FLASK_PORT" &>> "$LOG_FILE" &
else
    log_message "Flask app is already running."
fi

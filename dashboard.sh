#!/bin/bash

# Change to the directory where your Flask app is located
# cd /home/alphahub/development/SystemDashboard || { echo "Directory not found"; exit 1; }

# Create virtual environment if it doesn't exist; otherwise, activate it
eval "$(conda shell.bash hook)"

# Check if the conda environment exists
if ! conda env list | grep -q "systemdashboard"; then
    echo "Creating conda environment 'systemdashboard'"
    conda create -n systemdashboard python=3.10 -y
    echo "Activating conda environment 'systemdashboard'"
    conda activate systemdashboard
    echo "Installing required packages"
    pip install -r requirements.txt
else
    echo "Activating existing conda environment 'systemdashboard'"
    conda activate systemdashboard
fi

# Continue with the rest of your script
echo "Conda environment 'systemdashboard' is active."

# Export Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development  # or production

# Check if Flask app is running
if ! pgrep -f "flask run --host=0.0.0.0 --port=5050" > /dev/null; then
    echo "Flask app is not running. Starting..."
    flask run --host=0.0.0.0 --port=5050 &
else
    echo "Flask app is already running."
fi

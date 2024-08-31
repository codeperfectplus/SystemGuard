#!/bin/bash

# Function to add a cron job with error handling
add_cron_job() {
    # Define log directory and cron job command
    local username=$(whoami)
    local log_dir="/home/$username/logs"
    local cron_job="* * * * * /bin/bash $(pwd)/dashboard.sh >> $log_dir/systemguard_cron.log 2>&1"

    # Create log directory with error handling
    mkdir -p "$log_dir"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create log directory: $log_dir"
        exit 1
    fi

    # Verify user retrieval
    if [ -z "$username" ]; then
        echo "Error: Unable to retrieve current username."
        exit 1
    fi

    # Add cron job to crontab with error handling
    (crontab -l 2>/dev/null; echo "$cron_job") | crontab -
    if [ $? -ne 0 ]; then
        echo "Error: Failed to add the cron job to the crontab."
        exit 1
    fi

    echo "Cron job added: $cron_job"
}

# Call the function to add the cron job
add_cron_job

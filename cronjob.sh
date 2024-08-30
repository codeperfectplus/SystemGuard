#!/bin/bash

# Define the cron job command
username=$(whoami)
log_dir="/home/$username/logs"
mkdir -p "$log_dir"
CRON_JOB="* * * * * /bin/bash $(pwd)/dashboard.sh >> $log_dir/systemdashboard_cron.log 2>&1"

echo "Total cron jobs before: $(crontab -l | grep -v '^#' | wc -l)"

# Add the cron job to the crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job added: $CRON_JOB"

# show all cron jobs ignoring comments and empty lines

echo "Total cron jobs after: $(crontab -l | grep -v '^#' | wc -l)"




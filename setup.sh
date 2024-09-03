#!/bin/bash

# SystemGuard Installer Script
# ----------------------------
# This script installs, uninstalls, backs up, restores SystemGuard, and includes load testing using Locust.

# Determine the correct user's home directory
get_user_home() {
    if [ -n "$SUDO_USER" ]; then
        # When using sudo, SUDO_USER gives the original user who invoked sudo
        TARGET_USER="$SUDO_USER"
    else
        # If not using sudo, use LOGNAME to find the current user
        TARGET_USER="$LOGNAME"
    fi
    
    # Get the home directory of the target user
    USER_HOME=$(eval echo ~$TARGET_USER)
    echo "$USER_HOME"
}

# Set paths relative to the correct user's home directory
USER_HOME=$(get_user_home)
USER_NAME=$(echo $USER_HOME | awk -F'/' '{print $3}')
DOWNLOAD_DIR="/tmp"
EXTRACT_DIR="$USER_HOME/.systemguard"
LOG_DIR="$HOME/logs"
LOG_FILE="$LOG_DIR/systemguard-installer.log"
BACKUP_DIR="$USER_HOME/.systemguard_backup"
EXECUTABLE="/usr/local/bin/systemguard-installer"
LOCUST_FILE="$EXTRACT_DIR/SystemGuard-*/src/scripts/locustfile.py"
HOST_URL="http://localhost:5050"
INSTALLER_SCRIPT='setup.sh'
ISSUE_URL="https://github.com/codeperfectplus/SystemGuard/issues"
CRON_PATTERN=".systemguard/SystemGuard-.*/src/scripts/dashboard.sh"

# Create necessary directories
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_DIR"

# Logging function with timestamp
log() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a "$LOG_FILE"
}

# Check if running with sudo
if [ "$EUID" -eq 0 ]; then
    crontab_cmd="crontab -u $USER_NAME"
else
    crontab_cmd="crontab"
fi


# Function to add a cron job with error handling
add_cron_job() {

    # Define log directory and cron job command
    local log_dir="$USER_HOME/logs"
    local script_path=$(find "$EXTRACT_DIR" -name dashboard.sh)
    local cron_job="* * * * * /bin/bash $script_path >> $log_dir/systemguard_cron.log 2>&1"

    # Create log directory with error handling
    mkdir -p "$log_dir"
    if [ $? -ne 0 ]; then
        log "Error: Failed to create log directory: $log_dir"
        exit 1
    fi


    # Temporarily store current crontab to avoid overwriting on error
    local temp_cron=$(mktemp)
    if [ $? -ne 0 ]; then
        log "Error: Failed to create temporary file for crontab."
        exit 1
    fi

    # List the current crontab
    if ! $crontab_cmd -l 2>/dev/null > "$temp_cron"; then
        log "Error: Unable to list current crontab."
        rm "$temp_cron"
        exit 1
    fi

    # Ensure the cron job does not already exist
    if grep -Fxq "$cron_job" "$temp_cron"; then
        log "Cron job already exists: $cron_job"
        rm "$temp_cron"
        exit 0
    fi

    # Add the new cron job
    echo "$cron_job" >> "$temp_cron"
    if ! $crontab_cmd "$temp_cron"; then
        log "Error: Failed to add the cron job to crontab."
        rm "$temp_cron"
        exit 1
    fi

    rm "$temp_cron"
    log "Cron job added successfully: $cron_job"
}

# Backup function for existing configurations
backup_configs() {
    log "Backing up existing configurations..."
    if [ -d "$EXTRACT_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        cp -r "$EXTRACT_DIR" "$BACKUP_DIR/$(date '+%Y%m%d_%H%M%S')"
        log "Backup completed: $BACKUP_DIR"
    else
        log "No existing installation found to back up."
    fi
}

# Restore function to restore from a backup
restore() {
    log "Starting restore process..."
    
    # List available backups
    if [ -d "$BACKUP_DIR" ]; then
        echo "Available backups:"
        select BACKUP in "$BACKUP_DIR"/*; do
            if [ -n "$BACKUP" ]; then
                echo "You selected: $BACKUP"
                break
            else
                echo "Invalid selection. Please try again."
            fi
        done
        
        # Confirm restoration
        echo "Are you sure you want to restore this backup? This will overwrite the current installation. (y/n)"
        read CONFIRM
        if [ "$CONFIRM" != "y" ]; then
            log "Restore aborted by user."
            exit 0
        fi
        
        # Remove existing installation
        if [ -d "$EXTRACT_DIR" ]; then
            rm -rf "$EXTRACT_DIR"
            log "Old installation removed."
        fi
        
        # Restore selected backup
        cp -r "$BACKUP" "$EXTRACT_DIR"
        log "Restore completed from backup: $BACKUP"
    else
        log "No backups found to restore."
        echo "No backups found in $BACKUP_DIR."
    fi
}

# Function to install the script as an executable
install_executable() {
    # Use $0 to get the full path of the currently running script
    # CURRENT_SCRIPT=$(realpath "$0")
    cd $EXTRACT_DIR/SystemGuard-*/
    CURRENT_SCRIPT=$(pwd)/$INSTALLER_SCRIPT  
    # Verify that the script exists before attempting to copy
    if [ -f "$CURRENT_SCRIPT" ]; then
        log "Installing executable to /usr/local/bin/systemguard-installer..."
        cp "$CURRENT_SCRIPT" "$EXECUTABLE"
        log "Executable installed successfully."
    else
        log "Error: Script file not found. Cannot copy to /usr/local/bin."
    fi
}

# Install function
install() {
    log "Starting installation of SystemGuard..."
    echo "Enter the version of SystemGuard to install (e.g., v1.0.0 or 'latest' for the latest version):"
    read VERSION
    echo "Warning: This script will remove any existing installation of SystemGuard. Continue? (y/n)"
    read CONFIRM

    if [ "$CONFIRM" != "y" ]; then
        log "Installation aborted by user."
        exit 0
    fi

    # Fetch latest version if specified
    if [ "$VERSION" == "latest" ]; then
        log "Fetching the latest version of SystemGuard from GitHub..."
        VERSION=$(curl -s https://api.github.com/repos/codeperfectplus/SystemGuard/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
        if [ -z "$VERSION" ]; then
            log "Error: Unable to fetch the latest version. Please try again or specify a version manually."
            exit 1
        fi
        log "Latest version found: $VERSION"
    fi

    # Define URL after determining the version
    ZIP_URL="https://github.com/codeperfectplus/SystemGuard/archive/refs/tags/$VERSION.zip"
    log "Installing SystemGuard version $VERSION..."
    
    # Download the SystemGuard zip file
    log "Downloading SystemGuard version $VERSION from $ZIP_URL..."
    if ! wget -q "$ZIP_URL" -O "$DOWNLOAD_DIR/systemguard.zip"; then
        log "Error: Failed to download SystemGuard version $VERSION. Please check the version number and try again."
        exit 1
    fi
    log "Download completed successfully."

    # Backup existing configurations
    backup_configs

    # Remove any existing installation of SystemGuard
    log "Removing previous installation of SystemGuard, if any..."
    if [ -d "$EXTRACT_DIR" ]; then
        rm -rf "$EXTRACT_DIR"
        log "Old installation removed."
    fi

    # Clean up previous cron jobs related to SystemGuard
    log "Cleaning up previous cron jobs related to SystemGuard..."
    if $crontab_cmd -l | grep -q "$CRON_PATTERN"; then
        $crontab_cmd -l | grep -v "$CRON_PATTERN" | $crontab_cmd -
        log "Old cron jobs removed."
    else
        log "No previous cron jobs found."
    fi

    # Create the extraction directory
    log "Setting up installation directory..."
    mkdir -p $EXTRACT_DIR

    # Extract the downloaded zip file
    log "Extracting SystemGuard package..."
    unzip -q $DOWNLOAD_DIR/systemguard.zip -d $EXTRACT_DIR
    rm $DOWNLOAD_DIR/systemguard.zip
    log "Extraction completed."
    log "Preparing cronjob script..."
    add_cron_job

    # check if the cron job is added successfully
    if $crontab_cmd -l | grep -q "$CRON_PATTERN"; then
        log "Cron job added successfully."
    else
        log "Error: Failed to add the cron job."
        exit 1
    fi

    # Install the executable
    install_executable
    log "SystemGuard version $VERSION installed successfully!"
}

# Uninstall function
uninstall() {
    log "Uninstalling SystemGuard..."
    
    # Remove cron jobs related to SystemGuard
    # cronjob 

    if $crontab_cmd -l 2>/dev/null | grep -E "$CRON_PATTERN" > /dev/null; then
        echo "Are you sure you want to remove all cron jobs related to SystemGuard? (y/n)"
        read CONFIRM
        if [ "$CONFIRM" != "y" ]; then
            log "Uninstallation aborted by user."
            exit 0
        fi
        $crontab_cmd -l | grep -v "$CRON_PATTERN" | $crontab_cmd -
        log "Cron jobs removed."
    else
        log "No cron jobs found."
    fi

    # Remove the SystemGuard installation directory
    if [ -d "$EXTRACT_DIR" ]; then
        rm -rf "$EXTRACT_DIR"
        log "SystemGuard has been removed from your system."
    else
        log "SystemGuard is not installed on this system."
    fi

    # Remove the executable
    if [ -f "$EXECUTABLE" ]; then
        rm "$EXECUTABLE"
        log "Executable $EXECUTABLE removed."
    else
        log "No executable found to remove."
    fi
}

# Load test function to start Locust server
load_test() {
    log "Starting Locust server for load testing..."
    
    # Check if Locust is installed
    if ! command -v locust &> /dev/null
    then
        log "Locust is not installed. Please install it first."
        exit 1
    fi

    # Start Locust server
    log "Starting Locust server..."
    locust -f "$LOCUST_FILE" --host="$HOST_URL"
    # Optionally, you can pass additional Locust flags here if needed
    # locust -f "$LOCUST_FILE" --host="$HOST_URL" --headless -u 10 -r 1 --run-time 1m
}

# Check if SystemGuard is installed
check_status() {
    log "Checking SystemGuard status..."
    
    if [ -d "$EXTRACT_DIR" ]; then
        log "SystemGuard is installed at $EXTRACT_DIR."
    else
        log "SystemGuard is not installed."
    fi

    
    if $crontab_cmd '-l' | grep -q "$CRON_PATTERN"; then
        log "Cron job for SystemGuard is set."
    else
        log "No cron job found for SystemGuard."
    fi

    log "Performing health check on localhost:5005..."
    if curl -s --head $HOST_URL | grep "200 OK" > /dev/null; then
        log "SystemGuard services are running."
    else
        log "SystemGuard services are not running."
    fi
}

# Health check by pinging localhost:5005
health_check() {
    log "Performing health check on localhost:5005..."
    if curl -s --head $HOST_URL | grep "200 OK" > /dev/null; then
        log "Health check successful: $HOST_URL is up and running."
    else
        log "Health check failed: $HOST_URL is not responding."
    fi
}


# Display help
show_help() {
    echo "SystemGuard Installer"
    echo "Usage: ./installer.sh [options]"
    echo "Options:"
    echo "  --install           Install SystemGuard"
    echo "  --uninstall         Uninstall SystemGuard"
    echo "  --restore           Restore SystemGuard from a backup"
    echo "  --load-test         Start Locust load testing"
    echo "  --status            Check the status of SystemGuard installation"
    echo "  --health-check      Perform a health check on localhost:5005"
    echo "  --help              Display this help message"
}

# Parse command-line options
for arg in "$@"; do
    case $arg in
        --install) ACTION="install" ;;
        --uninstall) ACTION="uninstall" ;;
        --restore) ACTION="restore" ;;
        --load-test) ACTION="load_test" ;;
        --status) ACTION="check_status" ;;
        --health-check) ACTION="health_check" ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown option: $arg"; show_help; exit 1 ;;
    esac
done

# Execute based on the action specified
case $ACTION in
    install) install ;;
    uninstall) uninstall ;;
    restore) restore ;;
    load_test) load_test ;;
    install_latest) install_latest ;;
    check_status) check_status ;;
    health_check) health_check ;;
    *) echo "No action specified. Use --help for usage information." ;;
esac

# this script ran with sudo command so all the files have root permission 
# remove the root permission from the files to the user 
# Function to change ownership of a directory to the user
change_ownership() {
    local directory="$1"
    if [ -d "$directory" ]; then
        chown -R "$USER_NAME:$USER_NAME" "$directory"
    fi
}

# Call the change_ownership function
change_ownership "$EXTRACT_DIR"

echo "SystemGuard Installer script completed, Server may take a few minutes to start, if you face any try to restart the server."
echo "For any issues or feedback, please report at: $ISSUE_URL"
echo "For more information, check the log file: $LOG_FILE"
# End of script

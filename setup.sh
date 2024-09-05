#!/bin/bash

# SystemGuard Installer Script
# ----------------------------
# This script installs, uninstalls, backs up, restores SystemGuard, and includes load testing using Locust.
# Determine the correct user's home directory

# run this script with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this program with sudo."
    exit 1
fi

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
GIT_INSTALL_DIR="$EXTRACT_DIR/SystemGuard-dev"
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

# this function will change the ownership of the directory
# from root to the user, as the script is run as root
# and the installation directory should be owned by the user
change_ownership() {
    local directory="$1"
    if [ -d "$directory" ]; then
        # if permission is set to root then change it to the user
        if [ "$(stat -c %U "$directory")" == "root" ]; then
            chown -R "$USER_NAME:$USER_NAME" "$directory"
            log "Ownership changed from root to $USER_NAME for $directory"
        fi
    fi
}

# Function to create a directory if it does not exist
create_dir_if_not_exists() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir" || { log "Error: Failed to create directory: $dir"; exit 1; }
    fi
}

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
    log "Cron job added successfully" 
    log $cron_job
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

# remove previous installation of cron jobs and SystemGuard
remove_previous_installation() {
    log "Removing previous installation of SystemGuard, if any..."
    if [ -d "$EXTRACT_DIR" ]; then
        rm -rf "$EXTRACT_DIR"
        log "Old installation removed."
    fi

    log "Cleaning up previous cron jobs related to SystemGuard..."
    if $crontab_cmd -l | grep -q "$CRON_PATTERN"; then
        $crontab_cmd -l | grep -v "$CRON_PATTERN" | $crontab_cmd -
        log "Old cron jobs removed."
    else
        log "No previous cron jobs found."
    fi
}

# Function to fetch the latest version of SystemGuard from GitHub releases
fetch_latest_version() {
    log "Fetching the latest version of SystemGuard from GitHub..."
    VERSION=$(curl -s https://api.github.com/repos/codeperfectplus/SystemGuard/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
    if [ -z "$VERSION" ]; then
        log "Error: Unable to fetch the latest version. Please try again or specify a version manually."
        exit 1
    fi
    log "Latest version found: $VERSION"
}

# Function to download a release from a given URL
download_release() {
    local url=$1
    local output=$2
    log "Downloading SystemGuard from $url..."
    if ! wget -q "$url" -O "$output"; then
        log "Error: Failed to download SystemGuard. Please check the URL and try again."
        exit 1
    fi
    log "Download completed successfully."
}

# Function to setup the cron job for SystemGuard
setup_cron_job() {
    log "Preparing cron job script..."
    add_cron_job
    if $crontab_cmd -l | grep -q "$CRON_PATTERN"; then
        log "Cron job added successfully."
    else
        log "Error: Failed to add the cron job."
        exit 1
    fi
}

# Function to install the latest version of SystemGuard
install_from_git() {
    log "Installing SystemGuard from Git repository..."

    backup_configs
    remove_previous_installation

    log "Cloning the SystemGuard repository from GitHub..."
    if ! git clone https://github.com/codeperfectplus/SystemGuard.git "$GIT_INSTALL_DIR"; then
        log "Error: Failed to clone the repository. Please check your internet connection and try again."
        exit 1
    fi

    log "Repository cloned successfully."
    cd "$GIT_INSTALL_DIR" || { log "Error: Failed to navigate to the installation directory."; exit 1; }
    
    log "Setting up SystemGuard from Git repository..."
    install_executable

    log "SystemGuard installed successfully from Git!"
    setup_cron_job

    change_ownership "$EXTRACT_DIR"
    exit 0
}

# install the latest version of SystemGuard from the release
install_from_release() {
    echo "Enter the version of SystemGuard to install (e.g., v1.0.0 or 'latest' for the latest version):"
    read -r VERSION

    [ "$VERSION" == "latest" ] && fetch_latest_version

    ZIP_URL="https://github.com/codeperfectplus/SystemGuard/archive/refs/tags/$VERSION.zip"
    log "Installing SystemGuard version $VERSION..."

    download_release "$ZIP_URL" "$DOWNLOAD_DIR/systemguard.zip"

    backup_configs
    remove_previous_installation

    log "Setting up installation directory..."
    mkdir -p "$EXTRACT_DIR"

    log "Extracting SystemGuard package..."
    unzip -q "$DOWNLOAD_DIR/systemguard.zip" -d "$EXTRACT_DIR"
    rm "$DOWNLOAD_DIR/systemguard.zip"
    log "Extraction completed."

    install_executable
    setup_cron_job

    change_ownership "$EXTRACT_DIR"
    log "SystemGuard version $VERSION installed successfully!"
    log "Server may take a few minutes to start. If you face any issues, try restarting the server."
}

# Install function
install() {
    log "Starting installation of SystemGuard..."
    echo "Do you want to install from a Git repository or a specific release?"
    echo "1. Git repository"
    echo "2. Release"
    read -r INSTALL_METHOD

    case $INSTALL_METHOD in
        1)
            install_from_git
            ;;
        2)
            install_from_release
            ;;
        *)
            log "Invalid installation method. Please choose '1' for Git repository or '2' for Release."
            exit 1
            ;;
    esac
}
# Uninstall function
uninstall() {
    log "Uninstalling SystemGuard..."
    
    # Remove cron jobs related to SystemGuard
    # cronjob 
    remove_previous_installation
    
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

    log "Performing health check on $HOST_URL..."
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
# # End of script

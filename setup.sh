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
DOWNLOAD_DIR="/tmp"
EXTRACT_DIR="$USER_HOME/.systemguard/"
LOG_DIR="$HOME/logs"
LOG_FILE="$LOG_DIR/systemguard-installer.log"
BACKUP_DIR="$USER_HOME/.systemguard_backup"
EXECUTABLE="/usr/local/bin/systemguard-installer"
LOCUST_FILE="$EXTRACT_DIR/SystemGuard-*/src/scripts/locustfile.py"
HOST_URL="http://localhost:5050"
INSTALLER_SCRIPT='setup.sh'

echo "User: $(whoami)"
# Create necessary directories
mkdir -p "$LOG_DIR"
mkdir -p "$BACKUP_DIR"

# Logging function with timestamp
log() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a "$LOG_FILE"
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
    CRON_PATTERN=".systemguard/SystemGuard-.*/dashboard.sh"
    if crontab -l | grep -q "$CRON_PATTERN"; then
        crontab -l | grep -v "$CRON_PATTERN" | crontab -
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

    # Navigate to the setup directory and execute setup script
    log "Navigating to the SystemGuard setup directory..."
    cd $EXTRACT_DIR/SystemGuard-*/src/scripts
    if [ ! -f "cronjob.sh" ]; then
        log "Error: cronjob.sh not found in the extracted directory. Please verify the contents."
        exit 1
    fi

    # Make cronjob.sh executable and run it
    log "Preparing cronjob script..."
    chmod +x cronjob.sh
    log "Executing the cronjob setup..."
    ./cronjob.sh

    # Install the executable
    log "Installing executable to /usr/local/bin/systemguard-installer..."
    install_executable
    log "SystemGuard version $VERSION installed successfully!"
}

# Uninstall function
uninstall() {
    log "Uninstalling SystemGuard..."
    
    # Remove cron jobs related to SystemGuard
    log "Cleaning up cron jobs related to SystemGuard..."
    CRON_PATTERN=".systemguard/SystemGuard-.*/dashboard.sh"
    if crontab -l | grep -q "$CRON_PATTERN"; then
        crontab -l | grep -v "$CRON_PATTERN" | crontab -
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

# Display help
show_help() {
    echo "SystemGuard Installer"
    echo "Usage: ./installer.sh [options]"
    echo "Options:"
    echo "  --install      Install SystemGuard"
    echo "  --uninstall    Uninstall SystemGuard"
    echo "  --restore      Restore SystemGuard from a backup"
    echo "  --load-test    Start Locust load testing"
    echo "  --help         Display this help message"
}

# Parse command-line options
for arg in "$@"; do
    case $arg in
        --install) ACTION="install" ;;
        --uninstall) ACTION="uninstall" ;;
        --restore) ACTION="restore" ;;
        --load-test) ACTION="load_test" ;;
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
    *) echo "No action specified. Use --help for usage information." ;;
esac

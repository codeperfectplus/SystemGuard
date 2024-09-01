#!/bin/bash

LOG_FILE="/tmp/miniconda_installation.log"
MINICONDA_SCRIPT_URL="https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh"
MINICONDA_SCRIPT_PATH="/tmp/install_miniconda.sh"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

get_user_home() {
    if [ -n "$SUDO_USER" ]; then
        TARGET_USER="$SUDO_USER"
    else
        TARGET_USER="$LOGNAME"
    fi
    USER_HOME=$(eval echo ~$TARGET_USER)
    echo "$USER_HOME"
}

USER_HOME=$(get_user_home)
AUTO_CONFIRM=false

install_miniconda() {
    log "Starting Miniconda installation process."

    if [ "$AUTO_CONFIRM" = false ]; then
        echo "Do you want to install Miniconda? (y/n)"
        read -r answer
        if [ ! "$answer" = "y" ]; then
            log "Miniconda installation skipped by user."
            return
        fi
    else
        log "Auto-confirmation enabled, proceeding with installation."
    fi

    log "Downloading Miniconda installation script to /tmp directory."
    if wget "$MINICONDA_SCRIPT_URL" -O "$MINICONDA_SCRIPT_PATH"; then
        log "Miniconda installation script downloaded successfully."
    else
        log "Failed to download Miniconda installation script."
        return 1
    fi


    chmod +x "$MINICONDA_SCRIPT_PATH"
    
    log "Running Miniconda installation script."
    if "$MINICONDA_SCRIPT_PATH"; then
        log "Miniconda installation script executed successfully."
    else
        log "Miniconda installation script execution failed."
        return 1
    fi

    if [ -d "$USER_HOME/miniconda3" ]; then
        log "Miniconda installed successfully."
    else
        log "Miniconda installation failed."
        return 1
    fi

    log "Cleaning up installation files."
    rm "$MINICONDA_SCRIPT_PATH" || log "Failed to remove installation script."

    log "Miniconda installation process completed."
}

while getopts "y" opt; do
    case $opt in
        y) AUTO_CONFIRM=true ;;
        *) echo "Usage: $0 [-y]"; exit 1 ;;
    esac
done

install_miniconda

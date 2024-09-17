#!/bin/bash

# Script to set up Miniconda on a Linux system
# Status: Tested
# Published by: Deepak Raj
# Published on: 2024-08-28

# Function to determine the home directory of the target user
get_user_name() {
    if [ "$(whoami)" = "root" ]; then
        LOGNAME_USER=$(logname 2>/dev/null) # Redirect any error output to /dev/null
        if [ $? -ne 0 ]; then               # Check if the exit status of the last command is not 0
            echo "No login name found. Using fallback method."
            # use head -n 1 for native linux. tail -n 1 works with wsl.
            USER_NAME=$(cat /etc/passwd | grep '/home' | cut -d: -f1 | tail -n 1)
        else
            USER_NAME=$LOGNAME_USER
        fi
    else
        USER_NAME=$(whoami)
    fi
    echo "$USER_NAME"
}

USER_NAME=$(get_user_name)
USER_HOME="/home/$USER_NAME"
echo "User home directory: $USER_HOME"
INSTALL_PATH="$USER_HOME/miniconda3"
MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
TMP_INSTALLER="/tmp/$MINICONDA_INSTALLER"
MINICONDA_PAGE_URL="https://docs.anaconda.com/miniconda/"

# Function to extract the checksum from the Miniconda documentation page
extract_checksum() {
    echo "Downloading Miniconda documentation page..."
    wget -q "$MINICONDA_PAGE_URL" -O /tmp/miniconda_page.html

    if [ ! -f "/tmp/miniconda_page.html" ]; then
        echo "Failed to download Miniconda documentation page."
        return 1
    fi

    echo "Extracting checksum for $MINICONDA_INSTALLER..."
    CHECKSUM=$(grep -A 1 "$MINICONDA_INSTALLER" /tmp/miniconda_page.html | grep -oP '(?<=<span class="pre">)[a-f0-9]{64}(?=</span>)')

    rm /tmp/miniconda_page.html

    if [ -z "$CHECKSUM" ]; then
        echo "Checksum for $MINICONDA_INSTALLER not found."
        return 1
    fi
}

# Download Miniconda installer if it doesn't already exist
if [ -f "$TMP_INSTALLER" ]; then
    echo "Miniconda installer already exists in /tmp. Skipping download."
else
    echo "Downloading Miniconda installer..."
    wget https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER -O $TMP_INSTALLER
fi

# Verify the Miniconda installer checksum
echo "Verifying Miniconda installer..."
extract_checksum

if [ $? -ne 0 ]; then
    echo "Failed to extract checksum. Exiting..."
    exit 1
fi

DOWNLOAD_CHECKSUM=$(sha256sum $TMP_INSTALLER | awk '{print $1}')

echo "Checksum of downloaded file: $DOWNLOAD_CHECKSUM"
echo "Checksum from documentation: $CHECKSUM"

if [ "$DOWNLOAD_CHECKSUM" != "$CHECKSUM" ]; then
    echo "Checksum verification failed. Exiting..."
    echo "Do you want to proceed with the installation anyway? (y/n): "
    read proceed
    if [ "$proceed" != "y" ]; then
        echo "Exiting..."
        exit 1
    fi
fi

echo "Checksum verification successful."

# Check if Miniconda is already installed
echo $INSTALL_PATH

if [ -d "$INSTALL_PATH" ]; then
    echo "Miniconda is already installed at $INSTALL_PATH."
    read -p "Do you want to update Miniconda? (y/n): " update
    if [ "$update" != "y" ]; then
        echo "Exiting..."
        exit 0
    fi
    bash $TMP_INSTALLER -b -p $INSTALL_PATH -u
else
    # Run the Miniconda installer
    echo "Running Miniconda installer..."
    bash $TMP_INSTALLER -b -p $INSTALL_PATH
fi

# Initialize Miniconda
echo "Initializing Miniconda..."
$INSTALL_PATH/bin/conda init

# Clean up the installer
echo "Cleaning up..."
rm $TMP_INSTALLER

# Optional: Update Conda to the latest version
echo "Updating Conda..."
$INSTALL_PATH/bin/conda update -n base -c defaults conda -y

source ~/.bashrc

# Display final message
echo "Miniconda installation completed!"
echo "Miniconda is installed at $INSTALL_PATH"

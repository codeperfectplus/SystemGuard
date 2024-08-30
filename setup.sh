#!/bin/bash

# SystemGuard Installer Script
# ----------------------------
# This script installs SystemGuard by downloading the specified version from GitHub,
# cleaning up any previous installations, and setting up the new version.

# Variables
DOWNLOAD_DIR="/tmp"
EXTRACT_DIR="/home/$USER/.systemguard"

Prompt the user to enter the version of SystemGuard to install
echo "Enter the version of SystemGuard to install (e.g., v1.0.0 or 'latest' for the latest version):"
read VERSION

# If the user enters "latest", fetch the latest version number from GitHub
if [ "$VERSION" == "latest" ]; then
    echo "Fetching the latest version of SystemGuard from GitHub..."
    VERSION=$(curl -s https://api.github.com/repos/codeperfectplus/SystemGuard/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
    
    # Check if fetching the latest version was successful
    if [ -z "$VERSION" ]; then
        echo "Error: Unable to fetch the latest version. Please try again or specify a version manually."
        exit 1
    fi
    echo "Latest version found: $VERSION"
fi

# Define URL after determining the version
ZIP_URL="https://github.com/codeperfectplus/SystemGuard/archive/refs/tags/$VERSION.zip"

# Inform the user about the installation process
echo "Installing SystemGuard version $VERSION..."
echo "Downloading SystemGuard package from GitHub..."

# Download the SystemGuard zip file to the /tmp directory
wget -q $ZIP_URL -O $DOWNLOAD_DIR/systemguard.zip

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to download SystemGuard version $VERSION. Please check the version number and try again."
    exit 1
fi
echo "Download completed."

# Remove any existing installation of SystemGuard
echo "Removing previous installation of SystemGuard, if any..."
if [ -d "$EXTRACT_DIR" ]; then
    rm -rf "$EXTRACT_DIR"
    echo "Old installation removed."
fi

# Remove specific cron jobs related to previous SystemGuard installations
echo "Cleaning up previous cron jobs related to SystemGuard..."
CRON_PATTERN=".systemguard/SystemGuard-.*/dashboard.sh"
if crontab -l | grep -q "$CRON_PATTERN"; then
    # Remove only the lines that match the specific pattern
    crontab -l | grep -v "$CRON_PATTERN" | crontab -
    echo "Old cron jobs removed."
else
    echo "No previous cron jobs found."
fi

# Create the extraction directory
echo "Setting up installation directory..."
mkdir -p $EXTRACT_DIR

# Extract the downloaded zip file to the target directory
echo "Extracting SystemGuard package..."
unzip -q $DOWNLOAD_DIR/systemguard.zip -d $EXTRACT_DIR

# Remove the downloaded zip file to clean up
rm $DOWNLOAD_DIR/systemguard.zip
echo "Extraction completed."

Navigate to the extracted SystemGuard directory
echo "Navigating to the SystemGuard setup directory..."
cd $EXTRACT_DIR/SystemGuard-*/src/scripts

# Check if the cronjob.sh script exists in the extracted content
if [ ! -f "cronjob.sh" ]; then
    echo "Error: cronjob.sh not found in the extracted directory. Please verify the contents."
    exit 1
fi

# Make the cronjob.sh script executable
echo "Preparing cronjob script..."
chmod +x cronjob.sh

# Execute the cronjob.sh script to set up cron jobs and complete installation
echo "Executing the cronjob setup..."
./cronjob.sh

echo "SystemGuard version $VERSION installed successfully!"

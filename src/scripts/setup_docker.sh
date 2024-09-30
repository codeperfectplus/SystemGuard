#!/bin/bash

# Script to install Docker and Docker Compose on a Linux system
# status: tested
# published by: Deepak Raj
# published on: 2024-08-28

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or use sudo."
  exit 1
fi

# Update package lists
echo "Updating package lists..."
apt-get update -y

# Install necessary packages
echo "Installing packages for Docker installation..."
apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker’s official GPG key
echo "Adding Docker's official GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Set up the stable repository
echo "Setting up the Docker repository..."
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package lists again
echo "Updating package lists..."
apt-get update -y

# Install Docker
echo "Installing Docker..."
apt-get install -y docker-ce

# Fetch the latest Docker Compose version
echo "Fetching the latest Docker Compose version..."
LATEST_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')

# Install Docker Compose
echo "Installing Docker Compose version $LATEST_COMPOSE_VERSION..."
curl -L "https://github.com/docker/compose/releases/download/${LATEST_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Set executable permissions for Docker Compose
echo "Setting executable permissions for Docker Compose..."
chmod +x /usr/local/bin/docker-compose

# Add the current user to the Docker group without needing to input
echo "Adding user to Docker group..."
usermod -aG docker "$SUDO_USER"

# Restart Docker to apply changes
echo "Restarting Docker..."
systemctl restart docker

# Display final message
echo "Docker and Docker Compose installation completed!"
echo "Docker Compose version $LATEST_COMPOSE_VERSION installed."
echo "You might need to log out and log back in to apply the group changes."

# Optional: Print Docker and Docker Compose versions
echo "Docker version:"
docker --version
echo "Docker Compose version:"
docker-compose --version

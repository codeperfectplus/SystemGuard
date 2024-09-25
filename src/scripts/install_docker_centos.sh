#!/bin/bash

# Docker Installation Script for CentOS

# Exit script on any error
set -e

echo "Updating system packages..."
sudo yum update -y

echo "Installing required packages for Docker..."
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

echo "Adding Docker's official repository..."
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

echo "Installing Docker CE (Community Edition)..."
sudo yum install -y docker-ce docker-ce-cli containerd.io

echo "Starting Docker service..."
sudo systemctl start docker

echo "Enabling Docker to start on boot..."
sudo systemctl enable docker

echo "Verifying Docker installation..."
docker --version

echo "Running Docker Hello World test..."
sudo docker run hello-world

echo "Docker has been successfully installed and verified!"

# Optional: Add user to docker group for non-root usage
echo "Would you like to add your user to the Docker group to run Docker without sudo? (y/n)"
read -r add_to_docker_group

if [[ "$add_to_docker_group" == "y" ]]; then
    sudo usermod -aG docker $(whoami)
    echo "User added to Docker group. Please log out and log back in for changes to take effect."
fi

echo "Docker installation complete."

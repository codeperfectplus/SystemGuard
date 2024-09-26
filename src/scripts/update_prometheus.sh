#!/bin/bash

# function to get the user name
get_user_name() {
    if [ "$(whoami)" = "root" ]; then
        LOGNAME_USER=$(logname 2>/dev/null) # Redirect any error output to /dev/null
        if [ $? -ne 0 ]; then               # Check if the exit status of the last command is not 0
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
# Configuration
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CURRENT_DIR="$CURRENT_SCRIPT_DIR"
ROOT_DIR="$(dirname "$(dirname "$CURRENT_DIR")")"
PROMETHEUS_CONFIG_DIR="$ROOT_DIR/prometheus_config"
CONTAINER_NAME="prometheus"
PROMETHEUS_CONFIG="$PROMETHEUS_CONFIG_DIR/prometheus.yml"
PROMETHEUS_DATA_DIR="/home/$USER_NAME/.database/prometheus"
PROMETHEUS_IMAGE="prom/prometheus"  # Add your image name if needed
NETWORK_NAME="flask-prometheus-net"  # Specify your network name
PROMETHEUS_PORT="9090"  # Specify your port

# Logging function for better readability
log() {
    echo "[INFO] $1"
}

# Check if Prometheus container is running
if [ "$(docker ps -q -f name="$CONTAINER_NAME")" ]; then
    log "Stopping container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME"

    log "Starting container: $CONTAINER_NAME with new configuration"
    docker start "$CONTAINER_NAME"

    log "Reloading configuration for container: $CONTAINER_NAME"
    docker exec "$CONTAINER_NAME" kill -HUP 1  # Send SIGHUP to reload config
else
    log "Container $CONTAINER_NAME is not running. Starting a new container."
    docker run -d \
      --name "$CONTAINER_NAME" \
      --network "$NETWORK_NAME" \
      -p "$PROMETHEUS_PORT:$PROMETHEUS_PORT" \
      --restart always \
      -v "$PROMETHEUS_CONFIG:/etc/prometheus/prometheus.yml" \
      -v "$PROMETHEUS_DATA_DIR:/prometheus" \
      "$PROMETHEUS_IMAGE" &> /dev/null

    log "Prometheus container started successfully."
fi

log "Prometheus container has been updated with the new configuration."

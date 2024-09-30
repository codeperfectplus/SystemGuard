#!/bin/bash

# Set the path for the Alertmanager configuration file
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROMETHEUS_CONFIG_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")/prometheus_config"
ALERTMANAGER_CONFIG_FILE="$PROMETHEUS_CONFIG_DIR/alertmanager.yml"
IP_ADDRESS=$(hostname -I | awk '{print $1}')

# Create the Alertmanager configuration
cat > "$ALERTMANAGER_CONFIG_FILE" <<EOL
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
  receiver: 'systemguard-webhook'

  routes:
    - receiver: 'systemguard-webhook'

receivers:

  - name: 'systemguard-webhook'
    webhook_configs:
      - send_resolved: true
        url: 'http://$IP_ADDRESS:5050/alerts'
        max_alerts: 0  # Send all alerts in one webhook request

EOL

# Output message
echo "Alertmanager configuration initialized at $ALERTMANAGER_CONFIG_FILE"

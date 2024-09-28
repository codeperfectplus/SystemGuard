#!/bin/bash

# Set the path for the Alertmanager configuration file
ALERTMANAGER_CONFIG_FILE="prometheus_config/alertmanager.yml"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
# take slack_webhook from .env file
SLACK_WEBHOOK_URL=$(grep SLACK_WEBHOOK_URL .env | cut -d '=' -f2)

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

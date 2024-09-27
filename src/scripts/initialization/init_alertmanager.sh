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
  receiver: 'slack-notifications'  # Default receiver

  routes:
    - receiver: 'slack-notifications'
      continue: true  # This allows the alert to also be sent to the next receiver
    - receiver: 'systemguard-webhook'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - send_resolved: true
        api_url: '$SLACK_WEBHOOK_URL'
        channel: '#general'
        username: 'Alertmanager'
        icon_emoji: ':warning:'
        text: |
          *Alert:* {{ .CommonLabels.alertname }}
          *Instance:* {{ .CommonLabels.instance }}
          *Severity:* {{ .CommonLabels.severity }}
          *Description:* {{ .CommonAnnotations.description }}
          *Summary:* {{ .CommonAnnotations.summary }}

  - name: 'systemguard-webhook'
    webhook_configs:
      - send_resolved: true
        url: 'http://$IP_ADDRESS:5001/alerts'
        max_alerts: 0  # Send all alerts in one webhook request

EOL

# Output message
echo "Alertmanager configuration initialized at $ALERTMANAGER_CONFIG_FILE"

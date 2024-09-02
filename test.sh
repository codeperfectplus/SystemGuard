#!/bin/bash

# Get all IP addresses that are not loopback and not docker
ip_address=$(ip -o -4 addr show | grep -v '127.0.0.1\|docker0' | awk '{print $4}' | cut -d'/' -f1)

# Print the selected IP address
echo "Local IP address: $ip_address"

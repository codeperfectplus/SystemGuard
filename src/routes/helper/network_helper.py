import re

from flask import Flask, render_template, request, blueprints, jsonify
import subprocess

from src.config import app
from src.helper import get_ip_address


def scan_network(subnet):
    try:
        result = subprocess.run(
            ['nmap', '-sn', subnet],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_nmap_scan_network_output(result.stdout)
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

def scan_ports(ip_address):
    """
    Run an Nmap scan on the specified IP address to find open ports.
    ---
    Parameters:
        - ip_address: The IP address to scan.
    ---
    Returns:
        A list of dictionaries, where each dictionary represents
    """
    try:
        # Run Nmap to scan all ports on the specified IP address
        result = subprocess.run(
            ['nmap', ip_address],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_nmap_ports_output(result.stdout)
    except subprocess.CalledProcessError as e:
        return [{"port": "Error", "state": "N/A", "service": "N/A"}]

def parse_nmap_scan_network_output(output):
    # Initialize a list to hold scan results
    devices = []
    
    # Regex patterns for extracting device name, IP, and latency
    ip_pattern = re.compile(r'\b(\d{1,3}\.){3}\d{1,3}\b')
    latency_pattern = re.compile(r'latency\.\)(.*?)(\d+\.?\d*)s')  # TODO: Fix this regex pattern
    host_pattern = re.compile(r'Nmap scan report for (.+) \((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)')
    count_ports = 0

    # Split the output into lines and iterate through them
    lines = output.splitlines()
    current_device = None

    for line in lines:
        if "Nmap scan report for" in line:
            # Extract device name and IP address
            match = host_pattern.match(line)
            if match:
                device_name = match.group(1)
                ip_address = match.group(2)
                current_device = {"device": device_name, "ip": ip_address, "latency": "", "ports_searched": count_ports}
                devices.append(current_device)
        elif "Host is up" in line and current_device:
            # Extract latency
            latency_match = latency_pattern.search(line)
            if latency_match:
                current_device["latency"] = latency_match.group(2) + "s"
            else:
                current_device["latency"] = "Unknown"

    # Count the number of ports searched, Nmap generally scans 1000 ports if the port number is not specified
    count_ports = 1000

    # Update the port count for each device
    for device in devices:
        device['ports_searched'] = count_ports

    return devices

def parse_nmap_ports_output(output):
    # List to store parsed port scan results
    ports = []
    
    # Regex pattern for extracting port, state, and service
    port_pattern = re.compile(r'^(\d+/tcp)\s+(\w+)\s+(.+)$', re.MULTILINE)

    # Extract relevant data using regex
    for match in port_pattern.finditer(output):
        ports.append({
            "port": match.group(1),
            "state": match.group(2),
            "service": match.group(3)
        })
    
    return ports

def handle_network_scan():
    ip_address = get_ip_address()
    ip_address_with_mask = f"{ip_address}/24"
    scan_result = scan_network(ip_address_with_mask)
    return render_template(
        'experimental/scan.html', 
        network_result=scan_result, 
        ip_address=ip_address
    )

def handle_port_scan():
    ip_address = request.form['ip_address']
    scan_results = scan_ports(ip_address)
    return render_template(
        'experimental/scan.html', 
        port_results=scan_results, 
        ip_address=ip_address
    )


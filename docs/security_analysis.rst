Security Analysis
=================

SystemGuard includes a built-in **Security Analysis** feature designed to scan subnets for potential security vulnerabilities. This tool is essential for system administrators, developers, and DevOps engineers to proactively identify and address security risks within their network.

1. **Scan Subnet for Vulnerabilities**

   To perform a security scan of the subnet, follow these steps:

   - Go to the **Security Tools** section in the SystemGuard dashboard.
   - Select the **Security Analysis** tab.

2. **Subnet Device and Open Port Scan**

   You can scan the subnet to discover devices and their associated open ports:

   - Click on the **Scan** button to begin scanning the subnet.
   - The scan results will appear as a table displaying:
     
     - **IP Address** of each device
     - **Hostname**
     - A button to **View Open Ports** for each device.

3. **View Open Ports for a Specific Device**

   To check the open ports of a particular device:

   - Enter the **IP address** of the device in the search bar.
   - Click the **Scan Ports** button to display the open ports for that device.

This process allows you to efficiently monitor your network's security status and take appropriate actions to mitigate vulnerabilities.

4. **Enable/Disable Port**

   You can enable or disable a port for a specific device:

   - Click on the **Firewall** under the **Security Tools** section.
    - Enter the `Sudo Password` to go in ``SuperAdmin`` Mode.
    - Check the open ports for the local device.
    - Enter the `port number`, `protocol` and `action` to enable or disable the port.

The above security features are designed to enhance the security posture of your network and protect your systems from potential threats
and it's powered by `nmap` and `iptables` tools.

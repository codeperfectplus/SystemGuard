# SystemGuard 💂

System Guard is a Flask app designed to monitor server stats such as CPU, Memory, Disk, and Network. It also provides real-time monitoring capabilities which can be useful for system administrators, developers, and DevOps engineers to keep track of their server's performance and troubleshoot issues. The app uses the `psutil` library to retrieve system stats and the `speedtest-cli` library to perform a network speed test.

## Features 🚀

- Lightweight, open-source, and free to use with a straightforward installation process.
- Capable of monitoring core server metrics like CPU, memory, disk usage, and network traffic.
- Includes built-in security features such as authentication for login, logout, and signup.
- Administrators can manage user accounts by creating, updating, or deleting users.
- Admin-level access is required for configuring settings, managing users, and adjusting security and notification - preferences.
- Historical performance data can be viewed as charts, aiding in trend analysis.
- Supports network speed testing directly from the server.
- Provides the ability to terminate resource-heavy processes with a single command.
- Real-time server metric monitoring keeps data consistently updated.
- The interface is responsive and optimized for various devices including mobile, tablets, and desktops.
- The system can automatically update to the latest version to simplify maintenance.
- Installation can be done quickly via a bash script for easy setup.
- Notifications are sent to users and admins when a process is manually terminated.
- Offers website monitoring tasks that trigger email alerts when a website becomes unavailable.
- Configurable email alerts for various actions across the server.
- Role-based dashboards tailored for Developer, Admin, IT Manager, and Manager roles (upcoming feature).
- Option to download historical data in CSV format for detailed analysis (upcoming feature).
- Server status monitoring with alerts for server downtime or recovery (upcoming feature).


## Installation 🛠️

check the [Installation.md](/src/docs/installation.md) file for installation instructions.


## Email Feature 📧

| Email Alert | Is implemented | who will get the email |
| ----------- | -------------- | ---------------------- |
| Process Killed | Yes | Logged User |
| Login | Yes | Admin User and Logged User |
| Logout | Yes | Logged User |
| Signup | Yes | Admin User & signed up User |
| Create User | Yes | Admin User & Created User |
| Delete User | No | Admin User & Deleted User |
| Speed Test | Yes | Logged User |
| Server Up | Yes | Admin User |
| Notification Settings Change | Yes | Admin User |
| Signup | Yes(few changes required) | Admin User & Logged User |
| Website Monitoring | Yes | Input Email |
| Server Down | No | Admin User |
| Server Up | No | Admin User |


## Product Screenshots 📸

### HomePage

![HomePage](/src/static/images/dashboard.png)

### CPU Stats

![CPU Stats](/src/static/images/cpu.png)

### Memory Stats

![Memory Stats](/src/static/images/memory.png)

### Disk Stats

![Disk Stats](/src/static/images/disk.png)

### Speed Test

![Speed Test](/src/static/images/speedtest.png)

## Why not use a Docker image?

A Docker image has not been created for this project because it requires access to the host machine in order to retrieve server stats. Therefore, it is not possible to obtain server stats from within a Docker container.

## Upcoming Features 📅

- Receive notifications when system metrics cross predefined thresholds.
- Customizable dashboards for personalized server monitoring.
- Plugin support to enhance and extend SystemGuard's functionality.
- Generate and manage server logs for better tracking and troubleshooting.
- Monitor disk read/write speeds for performance insights.
- Check the current firewall status to ensure security.
- A dedicated website monitoring page for tracking uptime and performance.
- Track and save total network data sent/received in the database for data usage monitoring.

## Learnings 📖

- How to use the `psutil` library to retrieve system stats.
- How to use multiple Flask routes to display different pages.
- How to use multi-threading to run a function in the background.
- How to use the `chart.js` library to display charts on a webpage.
- How to use the `flask-login` library to manage user sessions.
- How to use the `flask-mail` library to send emails in Flask.

## Acknowledgments

| Project        | License             | Repository                                      |
| -------------- | ------------------- | ----------------------------------------------- |
| `speedtest-cli`| Apache License 2.0  | [GitHub repository](https://github.com/sivel/speedtest-cli) |
| `psutil`       | BSD 3-Clause License| [GitHub repository](https://github.com/giampaolo/psutil) |
| `flask`        | BSD 3-Clause License| [GitHub repository](https://github.com/pallets/flask) |
| `chart.js`     | MIT License         | [GitHub repository](https://github.com/chartjs/Chart.js) |


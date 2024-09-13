# Release Notes : SystemGuard

---

## SystemGuard v1.0.5 Pre Release

- Version: v1.0.5-pre
- Release Date: September 20, 2024
- Status: In Development

---

## SystemGuard v1.0.4 Release

- Version: v1.0.4
- Release Date: September 13, 2024
- Status: Stable

### Key Features

- **System Guard Fix:** Improved functionality for enhanced system monitoring.
- **Auto Update Feature:** Implemented automatic updates for seamless software maintenance.
- **Website Monitoring Enhancements:**
  - Added email alerts for website status.
  - Improved logic to track website uptime.
- **UI Enhancements:**
  - Lazy loading enabled on the homepage for better performance.
  - Flash messages added for improved user interaction.
- **Graphs:**
  - Enhanced graphs with improved refresh intervals and datetime display.
  - Added CPU, memory, network, and battery usage graphs.

### Fixes

- **Graph Bug:** Fixed issues with graph rendering on the frontend.
- **Logger Directory:** Resolved directory creation bugs in logging.
- **Setup Script:** Reverted changes causing memory issues and improved overall setup reliability.

### Improvements

- **ASCII Art & Flowchart:** Added to scripts for better user guidance.
- **Multi-threading:** Implemented for background tasks to improve performance.
- **Installation Instructions:** Refined for clarity and ease of use.
- **Dependency Updates:** Updated Flask and other dependencies in `requirements.txt`.

### Other Changes
- **Basic Firewall Added:** Initial firewall setup for enhanced security.
- **Code Refactoring:** Refined codebase, including JavaScript and installation scripts for better maintainability.

## Upgrade Instructions

It's recommended to upgrade to the latest version of SystemGuard to benefit from the new features and improvements, upgrade from release only for the stable version.

```
sudo systemguard-installer --install
```

## Known Issues

- **Firewall:** Basic firewall features are still in development and may not be fully functional.

---

## SystemGuard v1.0.4 Pre Release 

- Version: v1.0.4-pre
- Release Date: September 10, 2024
- Status: Pre-release

### New Features

- **System Fix Utility**: Added a dedicated fix feature to resolve system issues automatically.
- **Auto-Update**: SystemGuard now supports automatic updates to streamline the upgrade process.
- **Email Alerts**: Email notifications are triggered for website status changes (up/down).
- **Website Monitoring**: Enhanced logic to track website availability, with a new monitoring page and ping feature.
- **Lazy Loading**: Homepage optimized with lazy loading for faster performance.
- **Auto Browser Launch**: The browser now automatically opens post-installation.
- **Contribution Guidelines**: Added clear guidelines for contributing to the project.
- **Dynamic Titles**: Page titles now use dynamic variables for better customization.

### Improvements

- **Graph Updates**: Refined graphs for CPU, memory, network, and battery monitoring, with improved refresh intervals and axes.
- **Logging Enhancements**: Fixed logger directory issues and enhanced logging functionality.
- **Multithreading**: Background tasks now use multithreading for improved performance.
- **Firewall Integration**: Basic firewall features added for enhanced security.
- **Setup and Installation**: Several improvements to `setup.sh` and the installation script for smoother setup and error handling.
- **Codebase Refactoring**: Significant codebase refactoring to improve readability and performance.
  
### Fixes

- **Bug Fixes**: Multiple bug fixes including graph display and log directory issues.
- **Graph DateTime**: Improved DateTime display for graphs.
- **Installation Fixes**: Resolved installation script bugs for a seamless setup.

This release enhances stability, security, and performance while introducing new features for system monitoring and ease of use.

---

## SystemGuard v1.0.3 Release

- Version: v1.0.3
- Release Date: September 05, 2024
- Status: Stable

**Latest Improvements & Enhancements:**
- **Logging & Help Functions Revamped:** Enhanced logging for better visibility, and refined the help function for a more user-friendly experience.
- **Script Overhaul:** Major improvements to bash scripts, setup routines, and installation processes, making them more robust and efficient. This includes cleaning up cron jobs and removing old installations of SystemGuard.
- **SystemGuard Tweaks:** Fine-tuned installation and setup scripts for SystemGuard, enhancing overall stability and ease of use.
- **License Added:** A new LICENSE file has been introduced to the repository, setting clear guidelines for usage and contributions.

**Feature Additions & Fixes:**
- **Dashboard Updates:** Experimental dashboard features were added but later removed, keeping the focus on stability and user experience.
- **Email Functionality:** Enhanced email functions now better support new user sign-ups and notifications, making the system more responsive and user-friendly.
- **New Features & UI Enhancements:** Added refresh buttons and interval selectors for dashboards, along with toggles for various settings, ensuring more control and customization for users.
- **Model & Path Optimizations:** Updated file paths, model defaults, and system configurations to streamline user interactions and system performance.

**Continuous Refinement:**

- **Refactoring & Cleanup:** Continuous code refactoring and cleanup efforts to maintain a high standard of code quality, ensuring the system remains responsive and maintainable.
- **General Settings & Feature Toggles:** Expanded user context with new feature toggles and general settings, allowing for a more personalized user experience.

From tightening up scripts to rolling out new features, these updates reflect ongoing dedication to improving the application, one commit at a time!

---

## SystemGuard v1.0.2 Release

- Version: v1.0.2
- Release Date: September 02, 2024
- Status: deprecated

### Improvements

- Navigation Bar design improved to look more modern.
- Caching enabled for some settings that not going to change such as cpu core, max temperature
- checkbox added to enable/disable card on the dashboard

---

## SystemGuard v1.0.1 Release

- Version: v1.0.1
- Release Date: August 31, 2024
- Status: deprecated

### Improvements

- Installation of the SystemGuard is improved.
- bug fixes

---

## SystemGuard v1.0.0 Release

Version: v1.0.1
Release Date: August 30, 2024
Status: deprecated


System Guard is a Flask app designed to monitor server stats such as CPU, Memory, Disk, and Network. It also provides real-time monitoring capabilities which can be useful for system administrators, developers, and DevOps engineers to keep track of their server's performance and troubleshoot issues. The app uses the `psutil` library to retrieve system stats and the `speedtest-cli` library to perform a network speed test.

### Features

- Monitor server stats like CPU, Memory, Disk, and Network.
- Check the network speed of the server using a speed test.
- Rate limit the speed test to prevent abuse.
- Kill the process that is consuming the most CPU.
- Real-time monitoring of server stats.
- Responsive design that works on mobile, tablet, and desktop.

# SystemGuard 💂

System Guard is a Flask app designed to monitor server stats such as CPU, Memory, Disk, and Network. It also provides real-time monitoring capabilities which can be useful for system administrators, developers, and DevOps engineers to keep track of their server's performance and troubleshoot issues. The app uses the `psutil` library to retrieve system stats and the `speedtest-cli` library to perform a network speed test.

## Installation 🛠️

```bash
wget https://raw.githubusercontent.com/codeperfectplus/SystemGuard/main/setup.sh
chmod +x setup.sh && sudo mv setup.sh /usr/local/bin/systemguard-installer
```

### To install the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --install
```

### To uninstall the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --uninstall
```

### To Restore the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --restore
```

### Incase of any error, run the following command:

```bash
sudo systemguard-installer --fix
```


### Help
    
```bash
systemguard-installer --help
```


It will install the SystemGuard app and its dependencies in the crontab and it will be started automatically every time the server is restarted. The app will be available at `http://localhost:5050`.

## Dependencies(must be installed)

- Anaconda3/Miniconda3

```bash
# install miniconda3 if not installed already
wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh
chmod +x install_miniconda.sh && sudo ./install_miniconda.sh
```

## Features 🚀

- Monitor server stats like CPU, Memory, Disk, and Network.
- Check the network speed of the server using a speed test.
- Rate limit the speed test to prevent abuse.
- Kill the process that is consuming the most CPU.
- Real-time monitoring of server stats.
- Responsive design that works on mobile, tablet, and desktop.
- Update itself to the latest version.
- Easy download and installation using a bash script.
- Logged user and admin user will get the notification if the user kill some process manully on dashboard.
- Different email alerts for different actions.
- Different Dashboards for different users.(Deveoper, Admin, IT Manager, Manager)

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

- Threshold notifications
- Customizable dashboards
- Plugin support to make SystemGuard even more powerful.
- make server logs
- Check Disk read/write speed 
- Check Firewall status 

## Acknowledgments

| Project        | License             | Repository                                      |
| -------------- | ------------------- | ----------------------------------------------- |
| `speedtest-cli`| Apache License 2.0  | [GitHub repository](https://github.com/sivel/speedtest-cli) |
| `psutil`       | BSD 3-Clause License| [GitHub repository](https://github.com/giampaolo/psutil) |
| `flask`        | BSD 3-Clause License| [GitHub repository](https://github.com/pallets/flask) |
| `chart.js`     | MIT License         | [GitHub repository](https://github.com/chartjs/Chart.js) |


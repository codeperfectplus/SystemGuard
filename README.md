# SystemGuard

System Guard is a Flask app designed to monitor server stats such as CPU, Memory, Disk, and Network. It also provides real-time monitoring capabilities which can be useful for system administrators, developers, and DevOps engineers to keep track of their server's performance and troubleshoot issues. The app uses the `psutil` library to retrieve system stats and the `speedtest-cli` library to perform a network speed test.

## Installation 

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

### Help
    
```bash
systemguard-installer --help
```


It will install the SystemGuard app and its dependencies in the crontab and it will be started automatically every time the server is restarted. The app will be available at `http://localhost:5050`.

## Dependencies(must be installed)

- Anaconda3/Miniconda3

## Features

- Monitor server stats like CPU, Memory, Disk, and Network.
- Check the network speed of the server using a speed test.
- Rate limit the speed test to prevent abuse.
- Kill the process that is consuming the most CPU.
- Real-time monitoring of server stats.
- Responsive design that works on mobile, tablet, and desktop.
- Update itself to the latest version.
- Easy download and installation using a bash script.


## Product Screenshots

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

## Acknowledgments

| Project        | License             | Repository                                      |
| -------------- | ------------------- | ----------------------------------------------- |
| `speedtest-cli`| Apache License 2.0  | [GitHub repository](https://github.com/sivel/speedtest-cli) |
| `psutil`       | BSD 3-Clause License| [GitHub repository](https://github.com/giampaolo/psutil) |
| `flask`        | BSD 3-Clause License| [GitHub repository](https://github.com/pallets/flask) |
| `chart.js`     | MIT License         | [GitHub repository](https://github.com/chartjs/Chart.js) |


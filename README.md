# SystemDashboard

System Dashboard is a Flask app designed to monitor server stats such as CPU, Memory, Disk, and Network. It also provides real-time monitoring capabilities.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/codeperfectplus/SystemDashboard.git
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open the app in your browser:

```bash
http://localhost:5000
```

## Features

- Monitor server stats like CPU, Memory, Disk, and Network.
- Check the network speed of the server using a speed test.
- Rate limit the speed test to prevent abuse.

## Why not use a Docker image?

A Docker image has not been created for this project because it requires access to the host machine in order to retrieve server stats. Therefore, it is not possible to obtain server stats from within a Docker container.

## Acknowledgments

| Project        | License             | Repository                                      |
| -------------- | ------------------- | ----------------------------------------------- |
| `speedtest-cli`| Apache License 2.0  | [GitHub repository](https://github.com/sivel/speedtest-cli) |
| `psutil`       | BSD 3-Clause License| [GitHub repository](https://github.com/giampaolo/psutil) |
| `flask`        | BSD 3-Clause License| [GitHub repository](https://github.com/pallets/flask) |
| `chart.js`     | MIT License         | [GitHub repository](https://github.com/chartjs/Chart.js) |


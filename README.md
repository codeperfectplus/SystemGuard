# SystemDashboard

System Dashboard is flask app to monitor the server stats like CPU, Memory, Disk, Network etc. It also provides the option to monitor the server stats in real time.

## Installation

1. Clone the repository

```bash
git clone https://github.com/codeperfectplus/SystemDashboard.git
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python app.py
```

4. Open the app in your browser

```bash
http://localhost:5000
```

## Features

- Monitor the server stats like CPU, Memory, Disk, Network etc.
- Check the network speed of the server. (Speed test)
- Rate limit the speed test to avoid the abuse.

## Why not the docker image?

I have not created the docker image for this project because it requires the access to the host machine to get the server stats. So, it is not possible to get the server stats from the docker container.


## Acknowledgments
| Project | License | Repository |
|---------|---------|------------|
| `speedtest-cli` | Apache License 2.0 | [GitHub repository](https://github.com/sivel/speedtest-cli) |
| `psutil` | BSD 3-Clause License | [GitHub repository](https://github.com/giampaolo/psutil) |
| `flask` | BSD 3-Clause License | [GitHub repository](https://github.com/pallets/flask) |
| `chart.js` | MIT License | [GitHub repository](https://github.com/chartjs/Chart.js) |

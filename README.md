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


## Why not the docker image?

I have not created the docker image for this project because it requires the access to the host machine to get the server stats. So, it is not possible to get the server stats from the docker container.

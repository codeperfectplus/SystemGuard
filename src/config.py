import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


from src.logger import logger
from src.helper import get_system_node_name, get_ip_address
# from src.utils import get_ip_address, get_system_node_name

app = Flask(__name__)

# Application Metadata
APP_NAME = "SystemGuard"
DESCRIPTION = f"{APP_NAME} is a web application that allows you to monitor your system resources."
AUTHOR = "SystemGuard Team"
YEAR = "2024"
PRE_RELEASE = True
VERSION = "v1.0.5"
PROJECT_URL = f"https://github.com/codeperfectplus/{APP_NAME}"
CONTACT_EMAIL = ""
SYSTEM_NAME = get_system_node_name()
SYSTEM_IP_ADDRESS = get_ip_address()

HOME_DIR = os.path.expanduser("~")
DB_DIR = os.path.join(HOME_DIR, ".database")
os.makedirs(DB_DIR, exist_ok=True)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_DIR}/systemguard.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///systemguard.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define global variables for templates
app.jinja_env.globals.update(
    title=APP_NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    year=YEAR,
    version=VERSION,
    pre_release=PRE_RELEASE,
    project_url=PROJECT_URL,
    contact_email=CONTACT_EMAIL,
    system_name=SYSTEM_NAME,
    system_ip_address=SYSTEM_IP_ADDRESS,
)

def get_app_info():
    """Retrieve application metadata."""
    return {
        "title": APP_NAME,
        "description": DESCRIPTION,
        "author": AUTHOR,
        "year": YEAR,
        "version": VERSION,
        "pre_release": PRE_RELEASE,
        "project_url": PROJECT_URL,
        "contact_email": CONTACT_EMAIL,
        "system_name": SYSTEM_NAME,
        "system_ip_address": SYSTEM_IP_ADDRESS,
    }

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.logger import logger
from src.helper import get_system_node_name, get_ip_address, load_secret_key
# from src.utils import get_ip_address, get_system_node_name

app = Flask(__name__)

# Application Metadata
APP_NAME = "SystemGuard"
DESCRIPTION = f"{APP_NAME} is a web application that allows you to monitor your system resources."
AUTHOR = "SystemGuard Team"
YEAR = "2024"
PRE_RELEASE = False
VERSION = "v1.0.5"
PROJECT_URL = f"https://github.com/codeperfectplus/{APP_NAME}"
CONTACT_EMAIL = ""
SYSTEM_NAME = get_system_node_name()
SYSTEM_IP_ADDRESS = get_ip_address()
secret_key = load_secret_key()

HOME_DIR = os.path.expanduser("~")
DB_DIR = os.path.join(HOME_DIR, ".database")
os.makedirs(DB_DIR, exist_ok=True)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_DIR}/systemguard.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key
app.config['WTF_CSRF_SECRET_KEY'] = secret_key
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['WTF_CSRF_HEADER_NAME'] = "X-CSRFToken"
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access to cookies via JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"  # Prevent CSRF attacks via cross-site requests

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

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

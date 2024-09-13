import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from src.logger import logger
from src.helper import get_system_node_name, get_ip_address
# from src.utils import get_ip_address, get_system_node_name

app = Flask(__name__)

# Application Metadata
APP_NAME = "SystemGuard"
DESCRIPTION = f"{APP_NAME} is a web application that allows you to monitor your system resources."
AUTHOR = "Deepak Raj"
YEAR = "2024"
VERSION = "v1.0.4"
PROJECT_URL = f"https://github.com/codeperfectplus/{APP_NAME}"
CONTACT_EMAIL = ""
SYSTEM_NAME = get_system_node_name()
SYSTEM_IP_ADDRESS = get_ip_address()

HOME_DIR = os.path.expanduser("~")
DB_DIR = os.path.join(HOME_DIR, ".database")
os.makedirs(DB_DIR, exist_ok=True)
# systemguard path = /home/user/.database/systemguard.db

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_DIR}/systemguard.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# Define global variables for templates
app.jinja_env.globals.update(
    title=APP_NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    year=YEAR,
    version=VERSION,
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
        "project_url": PROJECT_URL,
        "contact_email": CONTACT_EMAIL,
        "system_name": SYSTEM_NAME,
        "system_ip_address": SYSTEM_IP_ADDRESS,
    }

# Initialize the database
db = SQLAlchemy(app)

@app.cli.command("run")
def server_start():
    """Log server start."""
    logger.info("Server started")

# Error Handlers
@app.errorhandler(403)
def forbidden(e):
    """Handle 403 Forbidden error."""
    return render_template("error/403.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 Not Found error."""
    return render_template("error/404.html"), 404

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed error."""
    return "Method not allowed", 405

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 Internal Server Error."""
    return "Internal server error", 500

@app.errorhandler(502)
def bad_gateway(e):
    """Handle 502 Bad Gateway error."""
    return "Bad gateway", 502

@app.errorhandler(503)
def service_unavailable(e):
    """Handle 503 Service Unavailable error."""
    return "Service unavailable", 503

class CustomError(Exception):
    """Custom exception for application-specific errors."""
    pass

# Optional: Request hooks
# @app.before_request
# def before_request_func():
#     """Function to run before each request."""
#     logger.info("This function runs before each request.")

# @app.after_request
# def after_request_func(response):
#     """Function to run after each request."""
#     logger.info("This function runs after each request.")
#     return response

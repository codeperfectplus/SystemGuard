from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from src.logger import logger

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///systemguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# define a variable to use in the templates
app.jinja_env.globals.update(
    title="SystemGuard",
    description="SystemGuard is a web application that allows you to monitor your system resources.",
    author="Deepak Raj",
    year="2024",
    version="1.0.4-pre-release",
    project_url="https://github.com/codeperfectplus/SystemGuard",
    contact_email="",
)

# Initialize the database
db = SQLAlchemy(app)

@app.cli.command("run")
def server_start():
    logger.info("Server started")

# 403 forbidden
@app.errorhandler(403)
def forbidden(e):
    """ 
    This function is called when a user tries to access a resource that they are not allowed to access.
    """
    return render_template("error/403.html"), 403

# not found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404

# 405 method not allowed
@app.errorhandler(405)
def method_not_allowed(e):
    return "Method not allowed", 405

# internal server error 500
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal server error", 500

# 502
@app.errorhandler(502)
def bad_gateway(e):
    return "Bad gateway", 502

# 503
@app.errorhandler(503)
def service_unavailable(e):
    return "Service unavailable", 503

class CustomError(Exception):
    pass



# Purpose: Run functions before or after each request, useful for tasks like logging, performance monitoring, or pre-processing requests
# @app.before_request
# def before_request_func():
#     logger.info("This function runs before each request.")

# @app.after_request
# def after_request_func(response):
#     logger.info("This function runs after each request.")
#     return response

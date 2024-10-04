import datetime
from flask import render_template, blueprints, request, redirect, url_for, flash
from flask_login import current_user

from src.config import app, logger

error_handlers_bp = blueprints.Blueprint("error_handlers", __name__)

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

@app.errorhandler(429)
def ratelimit_handler(e):
    return "Too many requests, please try again later.", 429

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

def days_until_password_expiry(user):
    return (user.password_last_changed + datetime.timedelta(days=60) - datetime.datetime.now()).days


@app.before_request
def check_password_expiry():
    # Allow access to login, password change, and static files routes without restriction
    if request.endpoint in ['login', 'change_password', 'static']:
        return

    # Perform checks only for authenticated users
    if current_user.is_authenticated:
        remaining_days = days_until_password_expiry(current_user)

        # Redirect if the password has expired
        if remaining_days <= 0:
            flash("Your password has expired. Please change it to continue.", "danger")
            return redirect(url_for('change_password'))

        # Warn the user if the password will expire soon
        if remaining_days <= 10:
            flash(f"Your password will expire in {remaining_days} days. Please change it soon.", "warning")

        # Check if the user is still using the default password (e.g., 'admin')
        if current_user.check_password("admin"):
            flash("Security Alert: Please change the default password for your security.", "danger")
            return redirect(url_for('change_password'))

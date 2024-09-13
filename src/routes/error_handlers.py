from flask import render_template, blueprints
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

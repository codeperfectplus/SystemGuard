import datetime
from src.config import app
from src import routes
from src.utils import render_template_from_file, get_flask_memory_usage, cpu_usage_percent, get_memory_percent
from src.models import UserProfile
from src.scripts.email_me import send_smpt_email

def register_routes():
    app.register_blueprint(routes.dashboard_bp)
    app.register_blueprint(routes.settings_bp)
    app.register_blueprint(routes.system_health_bp)
    app.register_blueprint(routes.cpu_info_bp)
    app.register_blueprint(routes.disk_info_bp)
    app.register_blueprint(routes.memory_info_bp)
    app.register_blueprint(routes.network_info_bp)
    app.register_blueprint(routes.speedtest_bp)
    app.register_blueprint(routes.process_bp)

app.config['is_server_up_email_sent'] = False

def server_up_email():
    with app.app_context():
        admin_emails = [user.email for user in UserProfile.query.filter_by(user_level="admin", receive_email_alerts=True).all()]
        if admin_emails:
            subject = "SystemGuard Server Started"
            context = {
                "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_usage": cpu_usage_percent(),
                "memory_usage": get_memory_percent(),
                "app_memory_usage": get_flask_memory_usage(),

            }
            html_body = render_template_from_file("src/templates/email_templates/server_up.html", **context)
            # send_smpt_email(admin_emails, subject, html_body, is_html=True)
            print("Server up email sent to", admin_emails)


if __name__ == "__main__":
    register_routes()
    # TODO: fix this email alert sent twice
    # if not app.config['is_server_up_email_sent']:
    #     app.config['is_server_up_email_sent'] = True
    #     server_up_email()
    
    # # Start the memory-consuming program in a separate thread
    # memory_thread = threading.Thread(target=memory_consuming_program, daemon=True)
    # memory_thread.start()
    
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)

from src.config import app, db
from src import routes

def register_routes():
    app.register_blueprint(routes.homepage_bp)
    app.register_blueprint(routes.settings_bp)
    app.register_blueprint(routes.system_health_bp)
    app.register_blueprint(routes.cpu_usage_bp)
    app.register_blueprint(routes.disk_usage_bp)
    app.register_blueprint(routes.memory_usage_bp)
    app.register_blueprint(routes.network_stats_bp)
    app.register_blueprint(routes.speedtest_bp)
    app.register_blueprint(routes.process_bp)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

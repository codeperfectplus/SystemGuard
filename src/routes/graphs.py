import subprocess
from flask import render_template, blueprints
from src.config import app
from src.routes.helper.common_helper import admin_required

graphs_bp = blueprints.Blueprint("graphs", __name__)

@app.route('/historical_system_metrics')
@admin_required
def historical_system_metrics():
    return render_template('graphs/graphs.html')


@app.route('/historical_alerts_metrics')
@admin_required
def historical_alerts_metrics():
    return render_template('graphs/alert_graphs.html')
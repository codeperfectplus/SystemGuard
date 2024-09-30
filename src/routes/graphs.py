import subprocess
from flask import render_template, blueprints
from src.config import app
from src.routes.helper.common_helper import admin_required

graphs_bp = blueprints.Blueprint("graphs", __name__)

@app.route('/historical_system_metrics')
@admin_required
def historical_system_metrics():
    return render_template('graphs/historical_system_metrics.html')


@app.route('/historical_alerts_metrics')
@admin_required
def historical_alerts_metrics():
    return render_template('graphs/historical_alerts_metrics.html')

#  bar graph 
# Compare the number of alerts across different instances and severity levels.
# multi bar based on severity

# Pie Chart
# Purpose: Show the proportion of different severity levels across all instances.


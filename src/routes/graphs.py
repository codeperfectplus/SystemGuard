import subprocess
from flask import render_template, blueprints
from src.config import app
from src.routes.helper.common_helper import admin_required

graphs_bp = blueprints.Blueprint("graphs", __name__)

@app.route('/graphs')
@admin_required
def graphs():
    return render_template('graphs/graphs.html')

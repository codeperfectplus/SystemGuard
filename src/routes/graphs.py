from flask import render_template, blueprints
from flask_login import login_required
from src.config import app

graphs_bp = blueprints.Blueprint("graphs", __name__)


@app.route('/graphs')
@login_required
def graphs():
    return render_template('graphs.html')

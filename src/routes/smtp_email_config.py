from flask_login import login_required
from flask import render_template, request, flash, redirect, url_for, blueprints

from src.config import app, db
from src.models import SmptEamilPasswordConfig

smtp_email_config_bp = blueprints.Blueprint('smtp_email_config', __name__)

@app.route("/update-email-password", methods=["GET", "POST"])
@login_required
def update_smpt_email_password():
    smtp_config = SmptEamilPasswordConfig.query.first()

    if request.method == "POST":
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        if not new_email or not new_password:
            flash("Please provide email and password.", "danger")
            return redirect(url_for("update_smpt_email_password"))
        
        
        if not smtp_config:
            smtp_config = SmptEamilPasswordConfig(email=new_email, password=new_password)
            db.session.add(smtp_config)
        else:
            smtp_config.email = new_email
            smtp_config.password = new_password        
        
        db.session.commit()
        flash("Email and password updated successfully!", "success")
        return redirect(url_for("update_smpt_email_password"))

    return render_template("update_smpt_email_password.html", smtp_config=smtp_config)

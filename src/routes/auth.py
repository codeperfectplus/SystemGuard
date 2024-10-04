import os
import datetime
from flask import render_template, redirect, url_for, request, blueprints, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.alert_manager import send_smtp_email
from src.config import app, db, limiter
from src.models import (
    UserProfile,
    UserCardSettings,
    PageToggleSettings,
    UserDashboardSettings,
)
from src.utils import render_template_from_file, ROOT_DIR
from src.routes.helper.common_helper import get_email_addresses
from src.config import get_app_info

auth_bp = blueprints.Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return UserProfile.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember_me = request.form.get("remember_me") == "on"  # TODO: Implement remember me
        

        user = UserProfile.query.filter(
            (UserProfile.username == username) | (UserProfile.email == username)
        ).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
 
            user.last_login = datetime.datetime.utcnow()
            user.save()

            if remember_me:
                login_manager.remember_cookie_duration = datetime.timedelta(days=7)
            else:
                login_manager.remember_cookie_duration = datetime.timedelta(0)

            receiver_email = current_user.email
            admin_emails_with_alerts = get_email_addresses(
                user_level="admin", receive_email_alerts=True
            )
            if admin_emails_with_alerts:
                if receiver_email in admin_emails_with_alerts:
                    admin_emails_with_alerts.remove(receiver_email)
                if admin_emails_with_alerts:
                    context = {
                        "username": current_user.username,
                        "login_time": datetime.datetime.now(),
                        "title": get_app_info()["title"]
                    }

                    login_alert_template = os.path.join(
                        ROOT_DIR, "src/templates/email_templates/admin_login_alert.html"
                    )
                    email_body = render_template_from_file(
                        login_alert_template, **context
                    )

                    send_smtp_email(
                        admin_emails_with_alerts,
                        "Login Alert",
                        email_body,
                        is_html=True,
                    )

            # # log in alert to user
            # if receiver_email:
            #     context = {
            #         "username": current_user.username,
            #         "login_time": datetime.datetime.now(),
            #     }

            #     login_message_template = os.path.join(
            #         ROOT_DIR, "src/templates/email_templates/login.html"
            #     )
            #     email_body = render_template_from_file(
            #         login_message_template, **context
            #     )

            #     send_smtp_email(receiver_email, "Login Alert", email_body, is_html=True)
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("auths/login.html")


@app.route("/logout")
def logout():
    # receiver_email = current_user.email
    # if receiver_email:
    #     context = {"username": current_user.username,
    #                "title": get_app_info()["title"]
    #                }
    #     logout_message_template = os.path.join(
    #         ROOT_DIR, "src/templates/email_templates/logout.html"
    #     )
    #     email_body = render_template_from_file(logout_message_template, **context)
    #     send_smtp_email(receiver_email, "Logout Alert", email_body, is_html=True)
    logout_user()
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        user_level = request.form.get(
            "user_level", "user"
        )  # Default to 'user' if not provided
        receive_email_alerts = (
            "receive_email_alerts" in request.form
        )  # Checkbox is either checked or not
        profession = request.form.get("profession", None)

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("signup"))

        existing_user = UserProfile.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        new_user = UserProfile(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password,
            user_level=user_level,
            receive_email_alerts=receive_email_alerts,
            profession=profession,
        )

        # Get Admin Emails with Alerts Enabled:
        admin_emails_with_alerts = get_email_addresses(
            user_level="admin", receive_email_alerts=True
        )
        if admin_emails_with_alerts:
            subject = "New User Alert"
            context = {
                "username": new_user.username,
                "email": new_user.email,
                "registration_time": datetime.datetime.now(),
                "user_level": new_user.user_level,
            }
            new_user_alert_template = os.path.join(
                ROOT_DIR, "src/templates/email_templates/new_user_alert.html"
            )
            email_body = render_template_from_file(new_user_alert_template, **context)
            send_smtp_email(admin_emails_with_alerts, subject, email_body, is_html=True)

        # Send email to the new user
        subject = f"Welcome to the {get_app_info()['title']}"
        context = {
            "username": new_user.username,
            "email": new_user.email,
        }
        welcome_template = os.path.join(
            ROOT_DIR, "src/templates/email_templates/welcome.html"
        )
        email_body = render_template_from_file(welcome_template, **context)
        send_smtp_email(email, subject, email_body, is_html=True)

        db.session.add(new_user)
        db.session.commit()
        db.session.add(UserDashboardSettings(user_id=new_user.id))
        db.session.add(UserCardSettings(user_id=new_user.id))
        db.session.add(PageToggleSettings(user_id=new_user.id))
        db.session.commit()
        flash("Account created successfully, please log in.")
        return redirect(url_for("login"))

    return render_template("auths/signup.html")

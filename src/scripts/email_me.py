import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import redirect, url_for, flash
from src.config import app
from src.logger import logger
from src.models import GeneralSettings, SMTPSettings
from src.config import get_app_info

system_name = os.uname().sysname

def send_smtp_email(receiver_email, subject, 
                    body, attachment_path=None, 
                    is_html=False, bypass_alerts=False):
        
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]  # Convert single address to list

    with app.app_context():
        if not bypass_alerts:
            general_settings = GeneralSettings.query.first()
            if general_settings:
                enable_alerts = general_settings.enable_alerts
                if not enable_alerts:
                    logger.info("Email alerts are disabled. Please enable them in the settings.")
                    flash("Email alerts are disabled. Please enable them in the settings.", "danger")
                    return redirect(url_for('general_settings'))
    
        email_password = SMTPSettings.query.first()
        if not email_password:
            logger.info("SMTP email credentials not found. Please set USER NAME and EMAIL_PASSWORD environment variables.")
            flash("SMTP email credentials not found. Please set USERNAME and EMAIL_PASSWORD environment variables.", "danger")
            return redirect(url_for('smtp_config'))

    USERNAME = email_password.username
    EMAIL_PASSWORD = email_password.password
    SMTP_SERVER = email_password.smtp_server
    SMTP_PORT = email_password.smtp_port
    EMAIL_FROM = email_password.email_from

    logger.info(f"Sending email to {receiver_email}")
    for email in receiver_email:
        try:
            server_name = os.uname().nodename

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM  # Must be a verified Elastic Email sender
            msg['To'] = email
            msg['Subject'] = f"{get_app_info()['title']} Alert from ({server_name}): {subject}"

            # Append message to the body
            append_message = f"This is an automated email from the {get_app_info()['title']} application. Please do not reply to this email."

            # Add HTML or plain text to the email body
            if is_html:
                full_body = body + f"<p>{append_message}</p>"
                msg.attach(MIMEText(full_body, 'html'))  # HTML content
            else:
                full_body = body + "\n\n" + append_message
                msg.attach(MIMEText(full_body, 'plain'))  # Plain text content

            # Attach a file if provided
            if attachment_path:
                try:
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(attachment_path)}",
                    )
                    msg.attach(part)
                except Exception as attach_error:
                    logger.warning(f"Attachment failed: {str(attach_error)}")
                    # You may decide to continue or fail here

            # Connect to the SMTP server (Elastic Email SMTP)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Secure connection
                server.login(USERNAME, EMAIL_PASSWORD)  # Elastic Email username (API key) and password

                # Send the email
                server.sendmail(EMAIL_FROM, email, msg.as_string())  # Use verified 'EMAIL_FROM'

            logger.info(f"Email sent successfully to {email}")
            # Continue sending to the next recipient, so no return here
        except Exception as e:
            logger.error(f"Failed to send email to {email}. Error: {str(e)}")
            # Log the error, continue with other emails
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

def send_smtp_email(receiver_email, subject, body, attachment_paths=None, 
                    is_html=False, bypass_alerts=False):
    """
    Function to send an SMTP email alert with optional attachment.

    :param receiver_email: List of recipient email addresses or a single email string.
    :param subject: Subject of the email.
    :param body: Body of the email (HTML or plain text).
    :param attachment_paths: List of file paths for attachments (optional).
    :param is_html: Boolean flag for HTML formatting in the email body.
    :param bypass_alerts: If True, bypass the general alert check settings.
    """

    # Convert single string receiver to list
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]

    with app.app_context():
        # Check if alerts are enabled, unless bypassing
        if not bypass_alerts:
            general_settings = GeneralSettings.query.first()
            if general_settings and not general_settings.enable_alerts:
                logger.info("Email alerts are disabled. Please enable them in the settings.")
                flash("Email alerts are disabled. Please enable them in the settings.", "danger")
                return redirect(url_for('general_settings'))

        # Fetch SMTP settings
        smtp_settings = SMTPSettings.query.first()
        if not smtp_settings:
            logger.info("SMTP email credentials not found. Please set USERNAME and EMAIL_PASSWORD.")
            flash("SMTP email credentials not found. Please set USERNAME and EMAIL_PASSWORD.", "danger")
            return redirect(url_for('smtp_config'))

    # Extract SMTP configuration details
    USERNAME = smtp_settings.username
    EMAIL_PASSWORD = smtp_settings.password
    SMTP_SERVER = smtp_settings.smtp_server
    SMTP_PORT = smtp_settings.smtp_port
    EMAIL_FROM = smtp_settings.email_from

    logger.info(f"Sending email to {receiver_email}")
    
    for email in receiver_email:
        try:
            server_name = os.uname().nodename

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM
            msg['To'] = email
            msg['Subject'] = f"{get_app_info()['title']} Alert from ({server_name}): {subject}"

            # Append application info to the message
            append_message = f"This is an automated email from the {get_app_info()['title']} application. Please do not reply."

            # Construct the email body (HTML or plain text)
            if is_html:
                full_body = f"<p>{body}</p><p>{append_message}</p>"
                msg.attach(MIMEText(full_body, 'html'))
            else:
                full_body = f"{body}\n\n{append_message}"
                msg.attach(MIMEText(full_body, 'plain'))

            # Handle multiple attachments
            if attachment_paths:
                for attachment_path in attachment_paths:
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
                        logger.warning(f"Failed to attach file {attachment_path}: {str(attach_error)}")

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(USERNAME, EMAIL_PASSWORD)
                server.sendmail(EMAIL_FROM, email, msg.as_string())

            logger.info(f"Email sent successfully to {email}")
        except Exception as e:
            logger.error(f"Failed to send email to {email}. Error: {str(e)}")

Alert Notifications Configuration
=================================

SystemGuard allows you to set up notifications for various system events using different communication channels like email, Slack, Discord, and Telegram. This helps ensure you are promptly notified when alerts are triggered.

Configuring Email Notifications
-------------------------------

SystemGuard supports sending email notifications via the SMTP protocol. To configure email alerts, follow these steps:

1. Navigate to the **SMTP Configurations** option under the **Settings** section in the SystemGuard dashboard.

2. Enter the following SMTP details:

   - **SMTP Server**: Provide the address of the SMTP server (e.g., `smtp.gmail.com`).
   - **SMTP Port**: Specify the port number for the SMTP server (e.g., `587` for TLS).
   - **SMTP Username**: Enter the username for authenticating with the SMTP server.
   - **SMTP Password**: Provide the password for the specified SMTP username.
   - **Sender Email**: Specify the email address from which the alerts will be sent.

3. After entering the details, save the configuration.

4. You can now receive email notifications when a system alert is triggered.

Configuring Slack Notifications
-------------------------------

SystemGuard can send alerts to Slack channels, allowing you to monitor alerts directly from your Slack workspace. To set up Slack notifications:

1. In the SystemGuard dashboard, go to the **Notifications** section.
   
2. Select **Slack Configurations** and enter the required webhook URL.
   
3. Assign the desired Slack channel for notifications and set the alert severity level (e.g., critical or warning).

4. Save the configuration, and SystemGuard will send alert notifications to the specified Slack channel.

Configuring Discord Notifications
---------------------------------

For Discord integration, SystemGuard supports sending alerts via webhooks. To configure Discord notifications:

1. Go to the **Notifications** section in SystemGuard's dashboard.

2. Select **Discord Configurations** and input the webhook URL generated from your Discord server.

3. Specify the channel where alerts should be sent, and customize the alert conditions as needed.

4. Save the settings. Alerts will now be sent to your Discord server when triggered.

Configuring Telegram Notifications
----------------------------------

To receive SystemGuard alerts on Telegram, follow these steps:

1. In the **Notifications** section of the SystemGuard dashboard, navigate to **Telegram Configurations**.

2. You will need to create a bot using **BotFather** on Telegram and obtain the bot token.

3. Enter the bot token and the chat ID of the Telegram group or user where alerts should be sent.

4. Configure the alert triggers and save the settings.

5. SystemGuard will send alerts to the specified Telegram chat.


General Settings
================

The **General Settings** section is the first place you'll encounter when navigating to the settings page in SystemGuard. Here, you can configure key options that define the server’s behavior and performance.

Timezone
~~~~~~~~

The **Timezone** setting allows you to specify the correct timezone for the server. This ensures that logs, events, and metrics are timestamped accurately.

To change the timezone:

1. Select the appropriate timezone from the dropdown menu.
2. Click **Save Changes** to apply the update.

Enable Caching
~~~~~~~~~~~~~~

The **Enable Caching** option allows you to control whether caching is active on the server. Caching can enhance performance by storing frequently accessed data, thus reducing server load.

- **Enabled**: Caching is activated, speeding up responses for repeat requests.
- **Disabled**: Caching is turned off, which may increase server load but ensures the most current data is always served.

Enable Alerts
~~~~~~~~~~~~~

The **Enable Alerts** setting allows you to toggle system alerts. When enabled, SystemGuard will notify you of critical events like high resource usage, system errors, or warnings.

- **Enabled**: Alerts will be sent to the configured email addresses or dashboards.
- **Disabled**: Alerts are disabled, and no notifications will be sent, even for critical issues.

Metrics Logging
~~~~~~~~~~~~~~~

The **Metrics Logging** option controls whether SystemGuard logs detailed system metrics. Enabling this feature allows for the recording of key metrics such as CPU, memory, and network usage for later analysis.

- **Enabled**: Metrics are logged, allowing for detailed performance reviews and historical analysis.
- **Disabled**: Metrics logging is turned off, reducing storage use but limiting insights into system performance.

Log Retention
~~~~~~~~~~~~~

The **Log Retention** setting determines how long logs will be stored before being automatically deleted. Adjust this to match your storage capabilities and compliance needs.

- **Retention Period**: Choose a retention period (e.g., 7 days, 30 days, or indefinitely).

Auto-Update
~~~~~~~~~~~

The **Auto-Update** setting controls whether SystemGuard updates automatically. If enabled, SystemGuard will periodically check for and install updates, ensuring your system stays current with the latest features and security patches.

- **Enabled**: SystemGuard will automatically download and install updates.
- **Disabled**: Updates must be manually installed.

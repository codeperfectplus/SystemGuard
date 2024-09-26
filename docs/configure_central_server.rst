Configure the Central Server
===========================

To configure the central server, you need to set up Prometheus to access data and metrics from other servers where SystemGuard is installed.

Steps to Configure:

1. Navigate to **SystemGuard Central** and click on **Configure Targets for SystemGuard**.

2. To add a new target, provide the following details:

   - **Job Name**: Enter a descriptive job name (e.g., `dev server`).
   - **Target URL**: Specify the target URL (e.g., `dev-server-ip:8000`).
   - **Scrape Interval**: Set the scrape interval (e.g., `10s`).
   - **Username**: Enter the Prometheus username for that server (any valid login will work).
   - **Password**: Enter the Prometheus password for that server (any valid login will work).

3. After entering the target details, click on the **Add Target** button to save the target.

4. Next, click on **Update Prometheus** to apply the changes in Prometheus.

5. Verify the changes in **Prometheus** or the **Dashboard Network** (within SystemGuard) to ensure everything is functioning correctly.

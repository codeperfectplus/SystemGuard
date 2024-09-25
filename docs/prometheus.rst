Prometheus Setup
================

Prometheus is a powerful monitoring and alerting toolkit designed for recording real-time metrics in a time-series database. It monitors server performance and can send alerts when issues arise.

By default, Prometheus is set up as a Docker service during the SystemGuard installation. To verify that Prometheus is running, open your browser and visit the following URL:

.. code-block:: bash

   http://localhost:9090

This will display the Prometheus dashboard.


To fetch data from the SystemGuard server, Prometheus requires a username and password for authentication. By default, these credentials are generated during the SystemGuard installation:

- **Default Username**: ``systemguard_admin``
- **Default Password**: ``systemguard_password``

Changing the Username and Password
----------------------------------

To change the default credentials, follow these steps:

1. Log in to the SystemGuard server using the default username and password.
2. Click on your profile icon in the top-right corner, then select **Change Password / Edit Profile**.
3. Enter the new username and password, then click **Save**.

Updating the Prometheus Configuration
-------------------------------------

After changing the credentials, you need to update the Prometheus configuration file. Follow these steps:

1. Navigate to the following URL on your SystemGuard server:

.. code-block:: bash

   /configure_targets

2. Enter the new username and password in the respective fields for the job name ``localhost`` (for the local server).
3. Click **Update** to apply the changes.
4. Prometheus will update within a few seconds.

Verification
------------

You can verify the changes by visiting the SystemGuard network dashboard on your SystemGuard server:

.. code-block:: bash

   /dashboard_network

The SystemGuard dashboard will display the instance status as **UP** if everything is functioning correctly.

API Endpoints Overview
=======================

System Information
------------------
- **Endpoint**: ``/api/v1/system-info``
- **Method**: ``GET``
- **Description**: Retrieve system metrics and performance data.

Historical Metrics Data
-----------------------
- **Endpoint**: ``/api/v1/prometheus/graphs_data/targets``
- **Method**: ``GET``
- **Description**: Fetch historical metrics data for specific targets.

SystemGuard/Prometheus Targets
------------------------------
- **Endpoint**: ``/api/v1/targets``
- **Method**: ``GET``
- **Description**: Retrieve a list of all monitoring targets in SystemGuard/Prometheus.

Refresh Interval
----------------
- **Endpoint**: ``/api/v1/refresh-interval``
- **Method**: ``GET``
- **Description**: Get the current refresh interval.

- **Endpoint**: ``/api/v1/refresh-interval``
- **Method**: ``POST``
- **Description**: Set or update the refresh interval.

OS Information
--------------
- **Endpoint**: ``/api/v1/os-info``
- **Method**: ``GET``
- **Description**: Get information about the operating system.

Prometheus Configuration
------------------------
- **Endpoint**: ``/api/v1/prometheus/config``
- **Method**: ``GET``
- **Description**: Retrieve the current Prometheus configuration.

- **Method**: ``POST``
- **Description**: Update the Prometheus configuration.

Prometheus Rules
----------------
- **Endpoint**: ``/api/v1/prometheus/rules``
- **Method**: ``GET``
- **Description**: Get the defined Prometheus rules.

- **Method**: ``POST``
- **Description**: Update the Prometheus rules.

Prometheus Ready
----------------
- **Endpoint**: ``/api/v1/prometheus/ready``
- **Method**: ``GET``
- **Description**: Check if Prometheus is ready.

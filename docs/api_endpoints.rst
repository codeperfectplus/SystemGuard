API Endpoints
=============

System Information
------------------

endpoint: /api/v1/system-info
method: GET
description: Get system metrics Information


Historical Metrics Data
-----------------------

endpoint: /api/v1/prometheus/graphs_data/targets
method: GET
description: Get historical metrics data for a target

SystemGuard/Prometheus Targets
-------------------

endpoint: /api/v1/targets
method: GET
description: Get all targets


Refresh interval
-------------------


endpoint: /api/v1/refresh-interval
method: GET
description: Get refresh interval

endpoint: /api/v1/refresh-interval
method: POST
description: Set refresh interval

Os Information
-------------------

endpoint: /api/v1/os-info
method: GET
description: Get os information

Prometheus Configuration
------------------------

endpoint: /api/v1/prometheus/config
method: GET
description: Get prometheus configuration

method: POST
description: Update prometheus configuration

Prometheus Rules
----------------

endpoint: /api/v1/prometheus/rules
method: GET
description: Get prometheus rules

method: POST
description: Update prometheus rules

Prometheus Ready 
----------------

endpoint: /api/v1/prometheus/ready
method: GET
description: Get prometheus ready status


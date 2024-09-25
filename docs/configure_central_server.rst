Congiure the Central Server
===========================

To configure the central server, you have to configure the prometheus to access data/metrics from the 
other servers on the node with systemguard installed.

1. Go to ``Systemguard Central`` and click on the ``configure targets for systemguard``.
2. To add new target add the follwing details:
   - Job Name: Enter the job name(eg: dev server)
   - Target URL: Enter the target url(eg: dev-server-ip:8000)
   - Scrap Interval: Enter the scrap interval(eg: 10s)
   - Username: Enter the prometheus username of that server(any login of that server will work)
    - Password: Enter the prometheus password of that server(any login of that server will work)
3. After adding the target, click on the ``add target`` button to add the target.
4. After this click on ``update prometheus`` to take the changes in effect on prometheus.
5. check on changes on ``prometheus`` or ``dashboard_network``(in systemguard) to see the changes.



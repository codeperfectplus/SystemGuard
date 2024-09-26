Other Useful Commands
=====================

Uninstallation
--------------

To uninstall the SystemGuard app from your system, use the following
command:

.. code:: bash

   sudo systemguard-installer --uninstall

This will remove SystemGuard and its related configurations from your
system.

----------

Fix Errors
----------

In case you encounter any errors or issues with the SystemGuard app, you
can attempt to fix them by running:

.. code:: bash

   sudo systemguard-installer --fix

This command will attempt to automatically fix any issues with the app.

--------------

Restore
-------

If you need to restore the SystemGuard app (e.g., after an improper
shutdown or system crash), you can run:

.. code:: bash

   sudo systemguard-installer --restore

This will restore the app to its previous functional state without
affecting its configurations.

--------------

Checking System Status
----------------------

To get a detailed report on the status of the SystemGuard app, including
its services, use the command:

.. code:: bash

   sudo systemguard-installer --status

--------------

Health Check
------------

To ensure that SystemGuard and its dependencies are running smoothly,
you can perform a system health check by running:

.. code:: bash

   sudo systemguard-installer --health

This will check various system resources and provide insights into the
overall health of your system.

--------------

Cleaning Backups
----------------

To clean up all the backups created by SystemGuard and free up disk
space, use the following command:

.. code:: bash

   sudo systemguard-installer --clean-backups

--------------

SystemGuard Logs
----------------

To check the logs for SystemGuard, which can be helpful for
troubleshooting or monitoring purposes, run:

.. code:: bash

   sudo systemguard-installer --logs

--------------

Stopping the SystemGuard Server
-------------------------------

If you need to stop the SystemGuard server, you can do so by running:

.. code:: bash

   sudo systemguard-installer --stop

--------------

Help
----

For a list of all available commands and their descriptions, run:

.. code:: bash

   sudo systemguard-installer --help

--------------

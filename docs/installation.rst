SystemGuard Guide
=================

Installation
------------

Prerequisites
~~~~~~~~~~~~~

Before installing SystemGuard, ensure that the following dependency is
installed:

-  **Anaconda3/Miniconda3**: This is required for the app to run
   properly.

To install Miniconda3, run the following commands:

.. code:: bash

   # Install Miniconda3
   wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh
   chmod +x install_miniconda.sh && ./install_miniconda.sh

Install Docker as it is required by the prometheus and grafana services.

.. code:: bash

   steps to install docker

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Install the required dependencies:

.. code:: bash

   # debian based distros
   sudo apt-get update
   sudo apt-get install git curl wget unzip iptables jq nmap

.. code:: bash

   sudo dnf update -y
   sudo dnf install -y git curl wget unzip iptables jq namp

.. code:: bash

   sudo yum update -y
   sudo yum install -y git curl wget unzip iptables jq nmap

-  curl: For downloading files from the internet.
-  wget: For downloading files from the internet.
-  unzip: For extracting zip files.
-  iptables: For managing firewall rules.
-  jq: For processing JSON data.
-  nmap: For network scanning and monitoring.

2. Download and set up the SystemGuard installer:

.. code:: bash

   wget https://raw.githubusercontent.com/codeperfectplus/SystemGuard/production/setup.sh
   chmod +x setup.sh && sudo mv setup.sh /usr/local/bin/systemguard-installer

3. Run the following command to install the SystemGuard app:

.. code:: bash

   sudo systemguard-installer --install

.. code:: bash

   # if above command doesn't work, try full path
   sudo /usr/local/bin/systemguard-installer --install

Uninstallation
--------------

To uninstall the SystemGuard app from your system, use the following
command:

.. code:: bash

   sudo systemguard-installer --uninstall

This will remove SystemGuard and its related configurations from your
system.

--------------

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

   systemguard-installer --help

--------------

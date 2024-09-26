SystemGuard Installation Guide
==============================


Installation
------------

Prerequisites
~~~~~~~~~~~~~

Before installing SystemGuard, ensure that the following dependency is
installed:

**Required Packages**
^^^^^^^^^^^^^^^^^^^^^

The following packages are required for the SystemGuard app to function
properly:

.. code:: bash

   sudo apt-get update
   sudo apt-get install git curl wget unzip iptables jq nmap

.. code:: bash

   sudo dnf update -y
   sudo dnf install -y git curl wget unzip iptables jq namp

.. code:: bash

   sudo yum update -y
   sudo yum install -y git curl wget unzip iptables jq nmap

**Anaconda3/Miniconda3**
^^^^^^^^^^^^^^^^^^^^^^^^

This is required for the app to run properly.

To install Miniconda3, run the following commands:

.. code:: bash

   # Install Miniconda3
   wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh
   chmod +x install_miniconda.sh && ./install_miniconda.sh

**Docker**
^^^^^^^^^^
Docker as it is required by the prometheus and grafana services. Install Docker using the following commands, based on your distro:

.. code:: bash

   # debian / apt based distros
   wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/refs/heads/main/setup/setup_docker.sh
   chmod +x setup_docker.sh && ./setup_docker.sh

.. code:: bash

   # centos / yum based distros
   wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/refs/heads/main/setup/setup_docker_centos.sh
   chmod +x setup_docker_centos.sh && ./setup_docker_centos.sh

Installation Steps
^^^^^^^^^^^^^^^^^^

1. Download and set up the SystemGuard installer:

.. code:: bash

   wget https://raw.githubusercontent.com/codeperfectplus/SystemGuard/production/setup.sh
   chmod +x setup.sh && sudo mv setup.sh /usr/local/bin/systemguard-installer

2. Run the following command to install the SystemGuard app:

.. code:: bash

   sudo systemguard-installer --install

.. code:: bash
   
   # if above command doesn't work, try full path
   sudo /usr/local/bin/systemguard-installer --install

3. Access the SystemGuard app by visiting the following URL in your
   browser:
   
.. code:: bash

   http://localhost:5050

.. note::

   Sign in with the default credentials:

   - default Username: ``admin``
   - default Password: ``admin``

.. note::
   
   It is recommended to change the default password after logging in.

4. Once logged in, you can start monitoring your server's performance.


SystemGuard Installation Guide
==============================

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

   wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/refs/heads/main/setup/setup_docker.sh
   chmod +x setup_docker.sh && ./setup_docker.sh

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

4. Access the SystemGuard app by visiting the following URL in your
   browser:
   
`http://localhost:5050 <http://localhost:5050>`_

5. Sign in with the default credentials:

   -  Username: admin
   -  Password: admin

6. Once logged in, you can start monitoring your server's performance.

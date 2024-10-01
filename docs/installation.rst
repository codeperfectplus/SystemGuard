SystemGuard Installation Guide
==============================

Prerequisites
~~~~~~~~~~~~~

Before installing **SystemGuard**, make sure the following dependencies
are installed.

**Required Packages**
^^^^^^^^^^^^^^^^^^^^^

The following packages are necessary for the proper functioning of the
SystemGuard application. Use the commands according to your operating
system.

For **Debian/Ubuntu** systems:

   .. code:: bash

      sudo apt-get update
      sudo apt-get install git curl wget unzip iptables jq nmap

For **Fedora** systems:

   .. code:: bash

      sudo dnf update -y
      sudo dnf install -y git curl wget unzip iptables jq nmap

For **CentOS/RHEL** systems:

   .. code:: bash

      sudo yum update -y
      sudo yum install -y git curl wget unzip iptables jq nmap

**Anaconda3/Miniconda3**
^^^^^^^^^^^^^^^^^^^^^^^^

**Miniconda3** or **Anaconda3** is required for the application to run
correctly. To install Miniconda3, execute the following commands:

   .. code:: bash

      wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh
      chmod +x install_miniconda.sh && ./install_miniconda.sh

**Docker**
^^^^^^^^^^

Docker is required to run **Prometheus** and **Grafana** services, which
are integral to the SystemGuard monitoring stack. Install Docker with
the following commands based on your distribution.

For **Debian/Ubuntu** systems:

   .. code:: bash

      wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/refs/heads/main/setup/setup_docker.sh
      chmod +x setup_docker.sh && sudo ./setup_docker.sh

For **CentOS/RHEL** systems:

   .. code:: bash

      wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/refs/heads/main/setup/setup_docker_centos.sh
      chmod +x setup_docker_centos.sh && sudo ./setup_docker_centos.sh

--------------

Installation Steps
~~~~~~~~~~~~~~~~~~

1. **Download and Set Up the SystemGuard Installer:**

   Use the following command to download the installer script:

   .. code:: bash

      wget https://raw.githubusercontent.com/codeperfectplus/SystemGuard/production/setup.sh
      chmod +x setup.sh && sudo mv setup.sh /usr/local/bin/systemguard-installer

2. **Install the SystemGuard App:**

   Run the installer to set up the SystemGuard app:

   .. code:: bash

      sudo systemguard-installer --install

   Optionally, you can install the Alert Manager along with the SystemGuard. Recommended for centralized server monitoring and alerting capabilities:

   .. code:: bash

      sudo systemguard-installer --install-alert-manager


3. **Access SystemGuard:**

   Once the installation is complete, open your browser and visit the
   following URL to access the SystemGuard dashboard:

   .. code:: bash

      http://localhost:5050

   .. Note:: 
      
      Use the default credentials to log in for the first time:

      -  **Username**: ``admin``
      -  **Password**: ``admin``

   .. caution::
      It is recommended that you change the default password after the
      initial login.

4. **Start Monitoring:**

   After logging in, you can begin monitoring your server’s performance
   and system metrics through the SystemGuard interface.

--------------

By following these steps, SystemGuard will be installed and ready for
use on your server.


.. Note::
   If the above command doesn’t work, try specifying the full path:

.. code:: bash

   sudo /usr/local/bin/systemguard-installer --install
## Installation 🛠️

```bash
wget https://raw.githubusercontent.com/codeperfectplus/SystemGuard/production/setup.sh
chmod +x setup.sh && sudo mv setup.sh /usr/local/bin/systemguard-installer
```

### To install the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --install
```

### To uninstall the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --uninstall
```

### To Restore the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --restore
```

### Incase of any error, run the following command:

```bash
sudo systemguard-installer --fix
```

### To know the status of the SystemGuard app, run the following command:

```bash
sudo systemguard-installer --status
```

### Run the health check for the SystemGuard app:

```bash
sudo systemguard-installer --health
```

### Clean up all the backups created by the SystemGuard app:

```bash
sudo systemguard-installer --clean-backups
```

### Check SystemGuard Server logs
    
```bash
sudo systemguard-installer --logs
```

### Stop SystemGuard Server
    
```bash
sudo systemguard-installer --stop
```

### Help
    
```bash
systemguard-installer --help
```


It will install the SystemGuard app and its dependencies in the crontab and it will be started automatically every time the server is restarted. The app will be available at `http://localhost:5050`.

## Dependencies(must be installed)

- Anaconda3/Miniconda3

```bash
# install miniconda3 if not installed already
wget https://raw.githubusercontent.com/codeperfectplus/HackScripts/main/setup/install_miniconda.sh
chmod +x install_miniconda.sh && sudo ./install_miniconda.sh
```
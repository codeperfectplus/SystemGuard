import os
import yaml
from src.utils import ROOT_DIR

prometheus_yml_path = os.path.join(ROOT_DIR, 'prometheus_config/prometheus.yml')

def is_valid_file(file_path: str) -> bool:
    """Checks if a file is valid and has key-value pairs separated by a colon."""
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if ':' not in line:
                return False
    return True

def load_yaml(file_path):
    """Load the YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    """Save the updated YAML data back to the file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def show_targets():
    """Show all targets for each job."""
    config = load_yaml(prometheus_yml_path)
    targets_info = []
    for scrape_config in config.get('scrape_configs', []):
        job_name = scrape_config['job_name']
        targets = scrape_config['static_configs'][0]['targets']
        scrape_interval = scrape_config.get('scrape_interval', '15s')
        targets_info.append({
            'job_name': job_name,
            'targets': targets,
            'scrape_interval': scrape_interval
        })
    return targets_info
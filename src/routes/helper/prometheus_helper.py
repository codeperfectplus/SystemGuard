import os
import yaml
import subprocess
from collections import OrderedDict
from src.utils import ROOT_DIR

prometheus_yml_path = os.path.join(ROOT_DIR, 'prometheus_config/prometheus.yml')
update_prometheus_path = os.path.join(ROOT_DIR, 'src/scripts/update_prometheus.sh')

def is_valid_file(file_path: str) -> bool:
    """Checks if a file is valid and has key-value pairs separated by a colon."""
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if ':' not in line:
                return False
    return True


class OrderedDumper(yaml.SafeDumper):
    """Custom YAML dumper that preserves order of keys."""
    pass

def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

OrderedDumper.add_representer(OrderedDict, dict_representer)

def load_yaml(file_path):
    """Load the YAML file and keep the order of dictionaries."""
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)

def save_yaml(data, file_path):
    """Save the updated YAML data back to the file, preserving order."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, Dumper=OrderedDumper, default_flow_style=False)

def update_prometheus_config():
    """Update the first target with the machine's IP address."""
    print("Updating Prometheus config...")
    
    # Get the machine's IP address
    try:
        ipv4_address = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True).stdout.split()[0]
    except subprocess.CalledProcessError as e:
        print(f"Error getting IP address: {e}")
        return False

    # Load the existing config
    try:
        config = load_yaml(prometheus_yml_path)
    except Exception as e:
        print(f"Error loading YAML config: {e}")
        return False

    # Fetch the 'localhost' job
    localhost_job = next((job for job in config.get('scrape_configs', []) if job.get('job_name') == 'localhost'), None)
    
    if localhost_job:
        # Update the IP address for the 'localhost' job target
        localhost_job['static_configs'][0]['targets'][0] = f'{ipv4_address}:5050'
        
        # Create a new OrderedDict to maintain the correct order
        updated_job = OrderedDict()
        updated_job['job_name'] = localhost_job['job_name']
        updated_job['scrape_interval'] = localhost_job.get('scrape_interval', '10s')
        updated_job['static_configs'] = localhost_job['static_configs']
        
        # Add basic_auth last to maintain order
        if 'basic_auth' in localhost_job:
            updated_job['basic_auth'] = localhost_job['basic_auth']

        # Replace the old job with the updated one
        for index, job in enumerate(config['scrape_configs']):
            if job['job_name'] == 'localhost':
                config['scrape_configs'][index] = updated_job
                break

        # Save the updated config
        try:
            save_yaml(config, prometheus_yml_path)
            print("Prometheus config updated successfully.")
            return True
        except Exception as e:
            print(f"Error saving YAML config: {e}")
            return False
    
    print("No 'localhost' job found in Prometheus config.")
    return False

def show_targets():
    """Show all targets for each job."""
    config = load_yaml(prometheus_yml_path)
    targets_info = []
    for scrape_config in config.get('scrape_configs', []):
        job_name = scrape_config['job_name']
        targets = scrape_config.get('static_configs', [{}])[0].get('targets', [])
        scrape_interval = scrape_config.get('scrape_interval', '15s')
        targets_info.append({
            'job_name': job_name,
            'targets': targets,
            'scrape_interval': scrape_interval
        })
    return targets_info

def update_prometheus_container():
    """Update the Prometheus container."""
    try:
        result = subprocess.run(['bash', update_prometheus_path], check=True, text=True, capture_output=True)
        print("Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while updating Prometheus container: {e}")
# check_requirements.py

import pkg_resources
import sys

def get_installed_packages():
    return {pkg.key for pkg in pkg_resources.working_set}

def read_requirements(file_path):
    with open(file_path, 'r') as f:
        return {line.strip().split('==')[0].lower() for line in f if line.strip() and not line.startswith('#')}

def main(requirements_file):
    installed_packages = get_installed_packages()
    required_packages = read_requirements(requirements_file)
    missing_packages = required_packages - installed_packages
    
    if missing_packages:
        print('\n'.join(missing_packages))
    else:
        print('All packages are installed.')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_requirements.py <requirements_file>")
        sys.exit(1)

    requirements_file = sys.argv[1]
    main(requirements_file)

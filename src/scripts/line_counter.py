import os
from collections import defaultdict

# Define the root directory of your project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
print(f"Root directory: {root_dir}")

# Function to count lines in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

# Step 1: Collect all extensions in the project
extensions = set()
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        file_ext = os.path.splitext(filename)[1].lower()  # Get file extension
        extensions.add(file_ext)

# Step 2: Define a function to categorize extensions into file types
def categorize_extension(ext):
    if ext in ['.py']:
        return 'Python'
    elif ext in ['.html', '.htm']:
        return 'HTML'
    elif ext in ['.sh']:
        return 'Shell'
    elif ext in ['.js']:
        return 'JavaScript'
    elif ext in ['.css']:
        return 'CSS'
    else:
        return 'Other'

# Step 3: Initialize a dictionary to store line counts by file type
line_counts = defaultdict(int)

# Step 4: Walk through the directory and count lines for each categorized file type
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        file_ext = os.path.splitext(filename)[1].lower()  # Get file extension
        file_path = os.path.join(dirpath, filename)
        
        file_type = categorize_extension(file_ext)
        line_counts[file_type] += count_lines_in_file(file_path)

# Print the results in a table format
print(f"{'File Type':<10} | {'Number of Lines':<15}")
print("-" * 30)
for file_type, count in line_counts.items():
    print(f"{file_type:<10} | {count:<15}")

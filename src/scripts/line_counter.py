import os

# Define the root directory of your project
root_dir = "."

# Define the file extensions to look for
file_types = {
    'Python': ['.py'],
    'HTML': ['.html', '.htm'],
    "Shell": ['.sh'],
    'JavaScript': ['.js'],
    'CSS': ['.css'],
    'Other': []  # Add other file types if needed
}

# Function to count lines in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

# Initialize counters for each file type
line_counts = {key: 0 for key in file_types}
line_counts['Other'] = 0  # Initialize 'Other' file type counter

# Walk through the directory and count lines
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        file_ext = os.path.splitext(filename)[1]
        file_path = os.path.join(dirpath, filename)
        
        # Determine the file type and update counts
        counted = False
        for file_type, extensions in file_types.items():
            if file_ext in extensions:
                line_counts[file_type] += count_lines_in_file(file_path)
                counted = True
                break
        
        # If the file type is not recognized, count under 'Other'
        if not counted:
            line_counts['Other'] += count_lines_in_file(file_path)

# Print the results in a table format
print(f"{'File Type':<10} | {'Number of Lines':<15}")
print("-" * 30)
for file_type, count in line_counts.items():
    print(f"{file_type:<10} | {count:<15}")

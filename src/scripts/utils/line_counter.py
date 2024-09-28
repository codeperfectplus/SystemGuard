import os
from collections import defaultdict

# Define the root directory of your project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Function to count lines in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

# Function to categorize extensions into file types
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
        return None  # Exclude 'Other'

# Initialize a dictionary to store line counts by file type
line_counts = defaultdict(int)

# Walk through the directory and count lines for each categorized file type
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        file_ext = os.path.splitext(filename)[1].lower()  # Get file extension
        file_type = categorize_extension(file_ext)
        if file_type:  # Only process known file types
            file_path = os.path.join(dirpath, filename)
            line_counts[file_type] += count_lines_in_file(file_path)

# Calculate total lines for percentage calculation
total_lines = sum(line_counts.values())

# Sort line counts by percentage in descending order
sorted_line_counts = sorted(line_counts.items(), key=lambda x: (x[1] / total_lines) if total_lines > 0 else 0, reverse=True)

print("## Line Counts by File Type", end='\n\n')
# Print the results in a Markdown table format with percentages
print("| File Type   | Number of Lines | Percentage |")
print("|-------------|-----------------|------------|")
for file_type, count in sorted_line_counts:
    percentage = (count / total_lines) * 100 if total_lines > 0 else 0
    print(f"| {file_type:<11} | {count:<15} | {percentage:>9.2f}% |")

# Print the total line count
print(f"| **Total**   | {total_lines:<15} | {'100.00%':>9} |")

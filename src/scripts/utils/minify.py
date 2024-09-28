import os
import htmlmin

def minify_html_file(file_path):
    # Read the original HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Minify the HTML content
    minified_content = htmlmin.minify(html_content, remove_comments=True, remove_empty_space=True)

    # Write the minified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(minified_content)
    print(f"Minified: {file_path}")

def find_and_minify_html_files(root_directory):
    # Walk through all directories and files
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                minify_html_file(file_path)

if __name__ == "__main__":
    # Get the current directory
    current_directory = os.getcwd()
    # Find and minify all HTML files
    find_and_minify_html_files(current_directory)

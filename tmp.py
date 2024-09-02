from flask import Flask, render_template_string


def render_template_from_file(template_file_path, **context):
    """
    Renders a Jinja template from a file with the given context and returns the rendered HTML content.

    :param template_file_path: Path to the template file to render.
    :param context: Context variables to pass to the template.
    :return: Rendered HTML content as a string.
    """
    # Open and read the template file content
    with open(template_file_path, 'r') as file:
        template_content = file.read()

    # Render the template content with the provided context
    rendered_html = render_template_string(template_content, **context)
    
    return rendered_html

context = {"username": "John Doe"}
output = render_template_from_file("src/templates/email_templates/login.html", **context)

print(output)
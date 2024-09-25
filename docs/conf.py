from datetime import datetime

# -- Project Information -----------------------------------------------------
project = 'SystemGuard'
author = 'SystemGuard Team'
version = '1.0.5'
year = datetime.now().year
copyright = f"{year} {author}"

# -- General Configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',          # Automatically document from docstrings
    'sphinx.ext.todo',             # Support for todo notes
    'sphinx.ext.coverage',         # Check documentation coverage
    'sphinx.ext.viewcode',         # Add links to highlighted source code
    'sphinx.ext.autosectionlabel'  # Allow reference links to sections automatically
]

# Prefix document path to section labels to avoid ambiguity
autosectionlabel_prefix_document = True

# PDF generation (requires an external tool for PDF build)
pdf_documents = [('index', u'SystemGuard Documentation', 'SystemGuard Docs', u'SystemGuard Team')]

# GitHub Releases Integration
releases_github_path = "codeperfectplus/systemguard"

# Templates path
templates_path = ['_templates']

# Source file format
source_suffix = ".rst"

# Main document
master_doc = "index"

# Patterns to exclude from the build
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']

# -- HTML Configuration ------------------------------------------------------
# Theme for HTML output
html_theme = 'sphinx_rtd_theme'  # Alternative themes: 'pydata_sphinx_theme', 'alabaster'

# Paths for custom static files (such as stylesheets)
# html_static_path = ['_static']

# Sidebar configuration
html_sidebars = {
    '**': [
        'globaltoc.html',  # Global table of contents
        'relations.html',  # Links to next/previous pages
        'sourcelink.html', # Link to source code
        'searchbox.html'   # Search box
    ]
}

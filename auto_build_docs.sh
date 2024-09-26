#!/bin/bash

# Set the directories for your Sphinx documentation source and build
SOURCE_DIR="docs"
BUILD_DIR="build"
PORT=5051

# remove the build directory
rm -rf "$BUILD_DIR"

# Check if sphinx-autobuild is installed
if ! command -v sphinx-autobuild &> /dev/null
then
    echo "sphinx-autobuild could not be found, installing it now..."
    pip install sphinx-autobuild
fi

# Run sphinx-autobuild with the source and build directories
echo "Starting auto-reload for Sphinx documentation..."
sphinx-autobuild "$SOURCE_DIR" "$BUILD_DIR" --open-browser --port "$PORT"

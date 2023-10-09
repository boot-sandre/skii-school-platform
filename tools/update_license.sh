#!/bin/bash

# Check if a search path argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <search_path>"
    exit 1
fi

# Path to your license file
LICENSE_FILE="tools/license-header.txt"
# Root path where need to use find
SEARCH_PATH="$1"  # Use the first command-line argument as the search path

# Check if the provided search path exists
if [ ! -d "$SEARCH_PATH" ]; then
    echo "Error: The specified search path '$SEARCH_PATH' does not exist."
    exit 1
fi

# Iterate over each Python source code file found within the search path
find "$SEARCH_PATH" -type f -name "*.py" | while read -r python_file; do
    # Concatenate the license text and Python source code file content
    cat "$LICENSE_FILE" "$python_file" > temp_python_file

    # Replace the original Python source code file with the updated content
    mv temp_python_file "$python_file"
done

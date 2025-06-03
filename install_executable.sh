#!/bin/bash

# Check if the ZIP file exists
if [ ! -f "build/output/compita-standalone.zip" ]; then
    echo "Error: compita-standalone.zip not found in build/output directory."
    echo "Please run './build_scripts/build_standalone.py' first to build the executable."
    exit 1
fi

# Extract the ZIP file to a temporary location
echo "Extracting the standalone executable..."
unzip -o build/output/compita-standalone.zip -d /tmp/compita-temp

# Create the bin directory if it doesn't exist
mkdir -p "$HOME/bin"

# Check if an existing executable or symlink exists and remove it
if [ -e "$HOME/bin/compita" ]; then
    echo "Removing existing compita executable or symlink..."
    rm "$HOME/bin/compita"
fi

# Copy the executable to the bin directory
echo "Copying new executable to $HOME/bin..."
cp /tmp/compita-temp/compita "$HOME/bin/"

# Make it executable
chmod +x "$HOME/bin/compita"

# Check if the PATH already includes $HOME/bin
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "Adding $HOME/bin to your PATH in .zshrc"
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.zshrc"
    echo "Please run 'source $HOME/.zshrc' to update your PATH"
else
    echo "$HOME/bin is already in your PATH"
fi

echo "Installation complete! You can now run 'compita' from anywhere."
echo "To verify the installation, run: which compita"
echo "To test the executable, run: compita --help"

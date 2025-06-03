#!/bin/bash
# CompITA Report Generator Installation Script
# This script installs the CompITA package with all its dependencies

# Set error handling
set -e

# Print banner
echo "============================================================"
echo "       CompITA Report Generator Installation Script         "
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Determine installation method
echo "Please select an installation method:"
echo "1. Install directly (system-wide or user)"
echo "2. Create a virtual environment (recommended)"
echo "3. Use uv for faster installation"
echo "4. Create a virtual environment with uv (fastest)"
read -p "Enter your choice (1-4): " CHOICE

case $CHOICE in
    1)
        echo "Installing CompITA package directly..."
        python3 -m pip install -e .
        ;;
    2)
        echo "Creating a virtual environment..."
        python3 -m venv compita-venv
        
        # Activate the virtual environment
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source compita-venv/Scripts/activate
        else
            source compita-venv/bin/activate
        fi
        
        echo "Installing CompITA package in the virtual environment..."
        pip install -e .
        
        echo "Virtual environment created at: $(pwd)/compita-venv"
        echo "To activate it in the future, run:"
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            echo "  source compita-venv/Scripts/activate"
        else
            echo "  source compita-venv/bin/activate"
        fi
        ;;
    3)
        echo "Installing with uv..."
        if ! command -v uv &> /dev/null; then
            echo "uv not found. Installing uv first..."
            python3 -m pip install uv
        fi
        uv pip install -e .
        ;;
    4)
        echo "Creating a virtual environment with uv..."
        if ! command -v uv &> /dev/null; then
            echo "uv not found. Installing uv first..."
            python3 -m pip install uv
        fi
        
        # Create and activate virtual environment with uv
        uv venv compita-venv
        
        # Activate the virtual environment
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source compita-venv/Scripts/activate
        else
            source compita-venv/bin/activate
        fi
        
        echo "Installing CompITA package in the virtual environment with uv..."
        uv pip install -e .
        
        echo "Virtual environment created at: $(pwd)/compita-venv"
        echo "To activate it in the future, run:"
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            echo "  source compita-venv/Scripts/activate"
        else
            echo "  source compita-venv/bin/activate"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Verify installation
echo "Verifying installation..."
if command -v compita &> /dev/null; then
    echo "✅ CompITA successfully installed!"
    echo "You can now use the 'compita' command."
    echo "For help, run: compita --help"
else
    echo "⚠️ Installation completed, but the 'compita' command is not in your PATH."
    echo "You may need to restart your terminal or add the Python bin directory to your PATH."
fi

echo "============================================================"
echo "Installation complete!"
echo "============================================================"

#!/usr/bin/env python3
"""
Build a standalone executable for the CompITA CLI using PyInstaller.
This script creates a single executable file that includes all dependencies.
"""
import os
import sys
import subprocess
import platform
import shutil
import tempfile
import venv

# Add the parent directory to the path to allow importing from the project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    """Build the standalone executable."""
    # Get the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Create build output directory
    build_output_dir = os.path.join(project_root, "build", "output")
    os.makedirs(build_output_dir, exist_ok=True)
    
    # Create a temporary virtual environment
    print("Creating virtual environment for building...")
    venv_dir = os.path.join(tempfile.gettempdir(), "compita_build_venv")
    
    # Remove existing venv if it exists
    if os.path.exists(venv_dir):
        print(f"Removing existing virtual environment at {venv_dir}")
        shutil.rmtree(venv_dir)
    
    # Create a new virtual environment
    print(f"Creating new virtual environment at {venv_dir}")
    venv.create(venv_dir, with_pip=True)
    
    # Determine the path to the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_executable = os.path.join(venv_dir, "bin", "python")
        pip_executable = os.path.join(venv_dir, "bin", "pip")
    
    # Install required dependencies in the virtual environment
    print("Installing required dependencies in virtual environment...")
    subprocess.run([pip_executable, "install", "pyinstaller", "pandas", "numpy", 
                   "openpyxl", "markdown", "weasyprint", "jinja2", "fastapi", "uvicorn", 
                   "python-multipart", "pydantic"], check=True)
    
    # Install the current package in development mode
    print("Installing current package in virtual environment...")
    os.chdir(project_root)  # Change to project root directory
    subprocess.run([pip_executable, "install", "-e", "."], check=True)
    
    # Determine the platform-specific executable name
    if platform.system() == "Windows":
        exe_name = "compita.exe"
    else:
        exe_name = "compita"
    
    # Define the entry point script
    entry_point = os.path.join(project_root, "compita-cli.py")
    
    # Define the PyInstaller command
    cmd = [
        os.path.join(os.path.dirname(pip_executable), "pyinstaller"),
        "--onefile",  # Create a single executable file
        "--name", exe_name,
        "--distpath", os.path.join(build_output_dir, "dist"),  # Custom dist directory
        "--workpath", os.path.join(build_output_dir, "work"),  # Custom work directory
        "--specpath", os.path.join(build_output_dir),  # Custom spec file directory
        "--add-data", f"{os.path.join(project_root, 'compita/templates')}:compita/templates",  # Include template files
        "--add-data", f"{os.path.join(project_root, 'compita/converters/templates')}:compita/converters/templates",  # Include converter templates
        "--add-data", f"{os.path.join(project_root, 'compita/src/web')}:compita/src/web",  # Include web interface files
        "--hidden-import", "pandas",
        "--hidden-import", "numpy",
        "--hidden-import", "openpyxl",
        "--hidden-import", "markdown",
        "--hidden-import", "weasyprint",
        "--hidden-import", "jinja2",
        "--hidden-import", "fastapi",
        "--hidden-import", "uvicorn",
        "--hidden-import", "pydantic",
        "--hidden-import", "python_multipart",
        entry_point  # The main script to build
    ]
    
    # Run PyInstaller
    print("Building standalone executable...")
    result = subprocess.run(cmd, check=False)
    
    if result.returncode != 0:
        print("Error: PyInstaller failed to build the executable.")
        print("Check the error messages above for details.")
        return 1
    
    # Create a distribution package
    print("Creating distribution package...")
    dist_dir = os.path.join(build_output_dir, "compita-dist")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Copy the executable
    shutil.copy(os.path.join(build_output_dir, "dist", exe_name), os.path.join(dist_dir, exe_name))
    
    # Copy assets directory
    assets_dir = os.path.join(project_root, "assets")
    if os.path.exists(assets_dir):
        shutil.copytree(assets_dir, os.path.join(dist_dir, "assets"), dirs_exist_ok=True)
    
    # Create a simple README
    with open(os.path.join(dist_dir, "README.txt"), "w") as f:
        f.write("CompITA Report Generator\n")
        f.write("=======================\n\n")
        f.write("This is a standalone executable that includes all dependencies.\n\n")
        f.write("Usage:\n")
        f.write(f"  ./{exe_name} generate-all --date YY-MM-DD\n")
        f.write(f"  ./{exe_name} --interactive\n\n")
        f.write("For more information, see the documentation.\n")
    
    # Create a ZIP file
    print("Creating ZIP archive...")
    zip_path = os.path.join(build_output_dir, "compita-standalone.zip")
    shutil.make_archive(os.path.join(build_output_dir, "compita-standalone"), "zip", dist_dir)
    
    # Print success message
    print(f"\nBuild successful! Distribution package created at: {os.path.abspath(zip_path)}")
    print("\nTo use the standalone executable:")
    print(f"1. Extract the ZIP file")
    print(f"2. Run the executable with: ./{exe_name} [command] [options]")
    print(f"   For example: ./{exe_name} generate-all --date 25-05-05")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

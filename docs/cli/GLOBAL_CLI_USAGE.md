# Running CompITA CLI From Anywhere on Your Mac

This guide explains how to run the CompITA CLI from any directory on your Mac.

## Option 1: Standalone Executable (Recommended)

The standalone executable approach bundles all dependencies into a single executable file, making it the most reliable and user-friendly option.

### Setup Process

1. Build the standalone executable:
   ```bash
   # From the project root directory
   ./build_scripts/build_standalone.py
   ```

2. Extract the ZIP file and copy the executable to your ~/bin directory:
   ```bash
   # Create ~/bin directory if it doesn't exist
   mkdir -p ~/bin
   
   # Extract the ZIP file to a temporary location
   unzip -o build/output/compita-standalone.zip -d /tmp/compita-temp
   
   # If you already have a previous version installed, remove it first
   if [ -e ~/bin/compita ]; then
     rm ~/bin/compita
   fi
   
   # Copy the executable to ~/bin
   cp /tmp/compita-temp/compita ~/bin/
   
   # Make it executable
   chmod +x ~/bin/compita
   ```

3. Ensure ~/bin is in your PATH by adding this line to your ~/.zshrc or ~/.bashrc:
   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

4. Apply the changes to your current shell:
   ```bash
   source ~/.zshrc  # or source ~/.bashrc if using bash
   ```

5. Verify the installation:
   ```bash
   # Check that the executable is in your PATH
   which compita
   
   # Should output something like: /Users/yourusername/bin/compita
   
   # Test the executable
   compita --help
   ```

### Troubleshooting

If you encounter issues during installation:

1. **Executable not found after installation**:
   - Ensure ~/bin is in your PATH: `echo $PATH | grep ~/bin`
   - If not found, manually add it to your current session: `export PATH="$HOME/bin:$PATH"`
   
2. **Permission denied when running the executable**:
   - Ensure the executable has the proper permissions: `chmod +x ~/bin/compita`

3. **Error when building the executable**:
   - Ensure you have PyInstaller installed: `pip install pyinstaller`
   - Check that all dependencies are installed: `pip install -e .`
   - If there are syntax errors in CLI files, fix them before building

4. **JSON file generation issues**:
   - Ensure the assets directory structure is correct
   - Check that the date format is correct (YY-MM-DD)
   - Verify that CSV files exist in the expected locations

### Usage

You can now run the CompITA CLI from anywhere on your Mac using the `compita` command:

```bash
# Show help
compita --help

# Run in interactive mode
compita --interactive

# Generate all reports for a specific date
compita generate-all --date 25-05-05

# Generate flexible module report
compita flexible-module --date 25-05-05 --all-modules 1 2 3

# Generate CSV module report
compita csv-module --date 25-05-05 --module 3
```

### Advantages of the Standalone Executable

- **Zero Dependencies**: All required libraries are bundled in the executable
- **Consistent Behavior**: Works the same way regardless of Python environment
- **Simple Maintenance**: Just rebuild and replace when code changes
- **Portability**: Can be moved to another machine with a compatible OS

## Option 2: Symlink Approach (Alternative)

This approach creates a symlink to the CLI script in your project directory. It's useful for development but requires Python and all dependencies to be installed.

### Setup

1. Make the CLI script executable:
   ```bash
   chmod +x compita-cli
   ```

2. Create a symlink in your ~/bin directory:
   ```bash
   ln -s /full/path/to/compita-report-python/compita-cli ~/bin/compita
   ```

3. Ensure ~/bin is in your PATH by adding this line to your ~/.zshrc or ~/.bashrc:
   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

### Usage

The usage is the same as with the standalone executable approach.

### Considerations for the Symlink Approach

- Requires Python and all dependencies to be installed
- Changes to the CLI script take effect immediately without rebuilding
- Useful for development and testing
- May encounter issues if dependencies are missing or incompatible

## Updating the Global CLI

### For Standalone Executable

```bash
# Rebuild the executable
./build_scripts/build_standalone.py

# Replace the existing executable
cp build/output/dist/compita ~/bin/
```

### For Symlink Approach

No update needed as the symlink points to the CLI script that you modify directly.

#!/usr/bin/env python3
"""Railway entrypoint script for Cyber8 Report Generator.
This script starts both the API and web servers in a way that works well in Railway's environment."""
import os
import subprocess
import signal
import sys
import time

def main():
    # Get the PORT from environment variable
    port = os.environ.get('PORT', '8000')
    
    print(f"Starting Cyber8 Report Generator with API on port {port}")
    
    # Start the API server using the CLI command
    api_cmd = [
        'python3', 'compita-cli.py', 'api',
        '--host', '0.0.0.0',
        '--port', port
    ]
    
    api_process = subprocess.Popen(api_cmd)
    
    # Wait a moment for the API server to start
    time.sleep(2)
    
    # Start the web server using the CLI command
    web_cmd = [
        'python3', 'compita-cli.py', 'web',
        '--host', '0.0.0.0',
        '--port', '8080',
        '--api-url', f'http://localhost:{port}'
    ]
    
    web_process = subprocess.Popen(web_cmd)
    
    print("Both API and web servers started successfully")
    
    # Function to handle termination signals
    def signal_handler(sig, frame):
        print("Received termination signal, shutting down servers...")
        web_process.terminate()
        api_process.terminate()
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Keep the main process running indefinitely
    # This ensures both child processes continue running even if one exits
    try:
        # Check processes periodically but don't exit if one fails
        while True:
            time.sleep(10)
            # Only log if a process has exited, but don't terminate the other
            if api_process.poll() is not None:
                print(f"API server exited with code {api_process.returncode}, but keeping web server running")
            if web_process.poll() is not None:
                print(f"Web server exited with code {web_process.returncode}, but keeping API server running")
    except KeyboardInterrupt:
        print("Received keyboard interrupt, shutting down servers...")
        web_process.terminate()
        api_process.terminate()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

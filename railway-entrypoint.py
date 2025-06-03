#!/usr/bin/env python3
"""
Railway entrypoint script for Cyber8 Report Generator.
This script starts both the API and web servers in a way that works well in Railway's environment.
"""
import os
import subprocess
import signal
import sys
import time

def main():
    # Get the PORT from environment variable
    port = os.environ.get('PORT', '8000')
    
    print(f"Starting Cyber8 Report Generator with API on port {port}")
    
    # Start the API server
    api_process = subprocess.Popen([
        'python3', 'compita-cli.py', 'api',
        '--host', '0.0.0.0',
        '--port', port
    ])
    
    # Wait a moment for the API server to start
    time.sleep(2)
    
    # Start the web server
    web_process = subprocess.Popen([
        'python3', 'compita-cli.py', 'web',
        '--host', '0.0.0.0',
        '--port', '8080',
        '--api-url', f'http://localhost:{port}'
    ])
    
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
    
    # Wait for processes to complete
    try:
        api_process.wait()
        print("API server exited, terminating web server...")
        web_process.terminate()
    except:
        pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

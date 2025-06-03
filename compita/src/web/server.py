#!/usr/bin/env python3
"""
Cyber8 Report Generator Web Server

This module provides a Flask web server for the Cyber8 Report Generator,
serving the web interface with Jinja2 templates and handling authentication
with ZITADEL.
"""

import os
import json
import argparse
import secrets
import time
import base64
import hashlib
from functools import wraps
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for, session, abort
from authlib.integrations.flask_oauth2 import ResourceProtector

from validator import ZitadelIntrospectTokenValidator, ValidatorError

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set secret key for session
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))

# Configuration
DEFAULT_API_URL = "http://localhost:8000"
API_URL = os.environ.get("API_URL", DEFAULT_API_URL)

# ZITADEL Configuration
ZITADEL_DOMAIN = os.environ.get("ZITADEL_DOMAIN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


# Setup resource protector
require_auth = ResourceProtector()
require_auth.register_token_validator(ZitadelIntrospectTokenValidator())

# Authentication helper functions
def is_token_expired():
    """Check if the access token has expired"""
    expiry = session.get('token_expiry')
    if not expiry:
        return True
    # Add a 30-second buffer to account for processing time
    return int(time.time()) > (expiry - 30)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('landing'))
        
        # Check if token is expired (for OAuth users)
        if session.get('auth_method') != 'direct' and is_token_expired():
            # Clear session and redirect to login
            session.clear()
            return redirect(url_for('landing', error='Your session has expired. Please log in again.'))
            
        return f(*args, **kwargs)
    return decorated_function

def get_login_url():
    """Generate ZITADEL login URL"""
    # Generate random state for CSRF protection
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    
    # Generate random nonce for replay protection
    nonce = secrets.token_hex(16)
    session['oauth_nonce'] = nonce
    
    # Build authorization URL for Basic authentication
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': url_for('callback', _external=True),
        'response_type': 'code',
        'scope': 'openid profile email',
        'state': state,
        'nonce': nonce
    }
    
    return f"{ZITADEL_DOMAIN}/oauth/v2/authorize?{urlencode(params)}"

# Landing page route
@app.route('/landing')
def landing():
    """Landing page - entry point for the application"""
    # Generate the ZITADEL login URL
    login_url = get_login_url()
    return render_template('landing.html', error=request.args.get('error'), login_url=login_url)

# Login route
@app.route('/login')
def login():
    """Login page"""
    # If user is already logged in, redirect to home
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    # Generate login URL
    login_url = get_login_url()
    
    # Display login page with error message if present
    return render_template('login.html', login_url=login_url, error=request.args.get('error'))

# Direct login route (username/password)
@app.route('/login_direct', methods=['POST'])
def login_direct():
    """Handle direct login with username/password"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # For demo purposes, accept hardcoded credentials
    if username == 'admin' and password == 'password':
        # Create a simple user object
        user = {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'roles': ['admin'],
            'picture': None,  # No profile picture for direct login users
            'auth_method': 'direct'
        }
        # Store user info in session (with consistent structure but no tokens)
        session['user'] = user
        session['access_token'] = None
        session['id_token'] = None  # No ID token for direct login
        session['refresh_token'] = None
        session['token_expiry'] = int(time.time()) + 3600  # 1 hour session
        return redirect(url_for('dashboard'))
    else:
        # Redirect to landing page with error message
        return redirect(url_for('landing', error='Invalid username or password. Try again or use ZITADEL SSO.'))

@app.route('/callback')
def callback():
    """OAuth callback route"""
    # Verify state to prevent CSRF
    state = request.args.get('state')
    if not state or state != session.get('oauth_state'):
        return redirect(url_for('landing', error='Invalid state parameter. Please try again.'))
    
    # Check for error in the callback
    error = request.args.get('error')
    error_description = request.args.get('error_description')
    if error:
        error_message = f"Authentication error: {error}"
        if error_description:
            error_message += f" - {error_description}"
        return redirect(url_for('landing', error=error_message))
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        return redirect(url_for('landing', error="No authorization code received."))
    
    # Prepare token request with Basic authentication
    token_url = f"{ZITADEL_DOMAIN}/oauth/v2/token"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': url_for('callback', _external=True)
    }
    
    # Make token request with Basic auth
    try:
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        token_response = requests.post(token_url, data=token_data, auth=auth)
        token_response.raise_for_status()
        tokens = token_response.json()
    except Exception as e:
        return redirect(url_for('landing', error=f"Error exchanging code for tokens: {str(e)}"))
    
    # Get user info
    try:
        userinfo_url = f"{ZITADEL_DOMAIN}/oidc/v1/userinfo"
        headers = {'Authorization': f"Bearer {tokens['access_token']}"}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
    except Exception as e:
        return redirect(url_for('landing', error=f"Error getting user info: {str(e)}"))
    
    # Store user info and tokens in session
    session['user'] = userinfo
    session['access_token'] = tokens['access_token']
    session['id_token'] = tokens.get('id_token')
    session['refresh_token'] = tokens.get('refresh_token')
    session['token_expiry'] = int(time.time()) + tokens.get('expires_in', 3600)
    session['auth_method'] = 'oauth'  # Mark this as an OAuth authentication
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Log out the user"""
    # Store the id_token before clearing the session
    id_token = session.get('id_token')
    
    # Clear local session
    session.clear()
    
    # If we have an ID token, redirect to ZITADEL end_session endpoint
    if id_token:
        params = {
            'id_token_hint': id_token,
            'client_id': CLIENT_ID,
            'post_logout_redirect_uri': url_for('landing', _external=True)
        }
        logout_url = f"{ZITADEL_DOMAIN}/oidc/v1/end_session?{urlencode(params)}"
        return redirect(logout_url)
    
    # If no ID token (direct login), just redirect to landing page
    return redirect(url_for('landing'))

@app.errorhandler(ValidatorError)
def handle_auth_error(ex):
    """Handle authentication errors"""
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@app.route('/')
def root():
    """Root route - redirect to landing page if not logged in, otherwise to dashboard"""
    current_user = session.get('user')
    if not current_user:
        return redirect(url_for('landing'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page"""
    current_user = session.get('user')
    return render_template('home.html', active_page='home', api_url=API_URL, current_user=current_user)

@app.route('/generate')
@login_required
def generate():
    """Render the generate reports page"""
    current_user = session.get('user')
    return render_template('generate.html', active_page='generate', api_url=API_URL, current_user=current_user)

@app.route('/upload')
@login_required
def upload():
    """Render the upload CSV page"""
    current_user = session.get('user')
    return render_template('upload.html', active_page='upload', api_url=API_URL, current_user=current_user)

@app.route('/reports')
@login_required
def reports():
    """Render the available reports page"""
    current_user = session.get('user')
    return render_template('reports.html', active_page='reports', api_url=API_URL, current_user=current_user)

@app.route('/flexible')
@login_required
def flexible():
    """Render the flexible reports page"""
    current_user = session.get('user')
    return render_template('flexible.html', active_page='flexible', api_url=API_URL, current_user=current_user)

@app.route('/setup')
@login_required
def setup():
    """Render the setup project page"""
    current_user = session.get('user')
    return render_template('setup.html', active_page='setup', api_url=API_URL, current_user=current_user)

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

@app.route('/api_url', methods=['GET'])
def get_api_url():
    """Return the API URL as JSON"""
    return jsonify({'api_url': API_URL})

@app.route('/api_url', methods=['POST'])
def set_api_url():
    """Set the API URL"""
    global API_URL
    data = request.get_json()
    if data and 'api_url' in data:
        API_URL = data['api_url']
        return jsonify({'success': True, 'api_url': API_URL})
    return jsonify({'success': False, 'error': 'Invalid request'})

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Cyber8 Report Generator Web Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind the server to')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help='URL of the API server')
    return parser.parse_args()

def main():
    """Main entry point for the web server"""
    args = parse_args()
    global API_URL
    API_URL = args.api_url
    app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    main()

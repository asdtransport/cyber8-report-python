#!/usr/bin/env python3
"""
Teaching Assistant Web Interface

This script provides a web interface for the teaching assistant chatbot.
"""

import os
import json
import subprocess
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import ta_chatbot
import time

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Initialize the chatbot
api_key = os.environ.get("OPENROUTER_API_KEY")
chatbot = None

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/reports')
def reports():
    """Render the reports page."""
    return render_template('reports.html')

# Create directories for reports and images
def create_directories():
    """Create necessary directories."""
    os.makedirs('reports', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)

@app.route('/download')
def download_file():
    """Download a file."""
    file_path = request.args.get('file')
    if not file_path:
        return jsonify({"error": "No file specified"}), 400
    
    # Security check to prevent directory traversal
    if '..' in file_path or file_path.startswith('/'):
        return jsonify({"error": "Invalid file path"}), 400
    
    # Determine the full path based on file type
    if file_path.endswith(('.png', '.jpg', '.jpeg')):
        full_path = os.path.join('static/images', file_path)
    else:
        full_path = os.path.join('reports', file_path)
    
    if not os.path.exists(full_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(full_path, as_attachment=True)

@app.route('/api/students')
def get_students():
    """Get a list of all students."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    # Get all students from the assessment data
    students = []
    for student in chatbot.assistant.assessment_data.get("students", []):
        students.append({
            "name": student.get("name", ""),
            "email": student.get("email", "")
        })
    
    return jsonify({"students": students})

@app.route('/api/at-risk')
def get_at_risk():
    """Get a list of at-risk students."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    at_risk = chatbot.assistant.identify_at_risk_students()
    return jsonify({"at_risk": at_risk})

@app.route('/api/modules')
def get_modules():
    """Get data for all modules."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    modules = {}
    for module in range(1, 7):
        modules[f"module_{module}"] = chatbot.assistant.get_module_progress(module)
    
    return jsonify({"modules": modules})

@app.route('/api/student/<name>')
def get_student(name):
    """Get data for a specific student."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        student_data = chatbot.get_student_data(name)
        return jsonify({"student": student_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/student-report')
def get_student_report_query():
    """Get a formatted report for a specific student using query parameter."""
    student_name = request.args.get('student')
    if not student_name:
        return jsonify({"error": "Student name is required"}), 400
    
    return get_student_report_data(student_name)

@app.route('/api/student/<student_name>/report')
def get_student_report(student_name):
    """Get a formatted report for a specific student using path parameter."""
    return get_student_report_data(student_name)

def get_student_report_data(student_name):
    """Helper function to get student report data."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    try:
        # Get the student data
        student_data = chatbot.get_student_data(student_name)
        
        # Format the report HTML
        html = f"""
        <div class="student-report">
            <div class="report-header mb-4">
                <h3>{student_data["name"]}</h3>
                <p>Email: {student_data["email"]}</p>
                <p>Overall Completion: {student_data["overall_completion"]:.1f}%</p>
                <p>Labs Completed: {student_data["labs_completed"]}/{student_data["total_labs"]}</p>
                <p>Average Assessment Score: {student_data["average_assessment_score"]:.1f}%</p>
            </div>
            
            <h4>Module Progress</h4>
            <div class="table-responsive mb-4">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>Module</th>
                            <th>Labs</th>
                            <th>Completion</th>
                            <th>Time Spent</th>
                            <th>Assessment</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add module rows
        for module in student_data["module_stats"]:
            html += f"""
                        <tr>
                            <td>{module["module"]}</td>
                            <td>{module["labs_completed"]}/{module["total_labs"]}</td>
                            <td>{module["completion_percentage"]:.1f}%</td>
                            <td>{module["time_spent_formatted"]}</td>
                            <td>{module["assessment_score"]:.1f}%</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            
            <h4>Recent Study Activity</h4>
            <div class="table-responsive mb-4">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>Date</th>
                            <th>Time Spent</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add study pattern rows
        for pattern in student_data["study_patterns"][-5:]:  # Show last 5 entries
            html += f"""
                        <tr>
                            <td>{pattern["date"]}</td>
                            <td>{pattern["time_spent_formatted"]}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            
            <h4>Recommendations</h4>
            <ul class="list-group mb-4">
        """
        
        # Add recommendations
        for recommendation in student_data["recommendations"]:
            html += f"""
                <li class="list-group-item">{recommendation}</li>
            """
        
        html += """
            </ul>
        </div>
        """
        
        return jsonify({"report": html})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message."""
    global chatbot
    if not chatbot:
        return jsonify({"error": "Chatbot not initialized"}), 500
    
    data = request.json
    query = data.get('query', '')
    student_name = data.get('student', None)
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Get student data if a student is selected
    student_data = None
    if student_name:
        try:
            student_data = chatbot.get_student_data(student_name)
        except Exception as e:
            return jsonify({"error": f"Error finding student: {str(e)}"}), 404
    
    # Process the query with the LLM
    response = chatbot.query_llm(query, student_data)
    
    return jsonify({
        "query": query,
        "response": response,
        "student": student_name
    })

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate a report based on the request."""
    data = request.json
    report_type = data.get('report_type')
    
    if not report_type:
        return jsonify({"error": "Report type is required"}), 400
    
    # Get common parameters
    current_module = data.get('current_module', '6')
    
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        if report_type == 'module':
            module_number = data.get('module_number')
            student_name = data.get('student_name')
            
            if not module_number:
                return jsonify({"error": "Module number is required"}), 400
            
            if module_number == 'all':
                # Generate reports for all modules
                cmd = [
                    'python', 'generate_reports.py',
                    '--current-module', current_module
                ]
                
                for i in range(1, 7):
                    output_path = f'reports/module{i}_report.csv'
                    cmd.extend(['--module', str(i), '--output', output_path])
                
                file_path = 'module_reports.zip'
                output_msg = "Generated reports for all modules"
            else:
                # Generate report for a specific module
                output_path = f'reports/module{module_number}_report.csv'
                
                cmd = [
                    'python', 'generate_reports.py',
                    '--module', module_number,
                    '--current-module', current_module,
                    '--output', output_path
                ]
                
                if student_name:
                    cmd.extend(['--student', student_name])
                
                file_path = output_path
                output_msg = f"Generated report for Module {module_number}"
            
        elif report_type == 'class':
            # Generate class report
            output_path = 'reports/class_report.csv'
            
            cmd = [
                'python', 'generate_reports.py',
                '--class',
                '--current-module', current_module,
                '--output', output_path
            ]
            
            file_path = output_path
            output_msg = "Generated class report"
            
        elif report_type == 'excel':
            # Generate Excel report
            output_path = 'reports/student_progress_report.xlsx'
            
            cmd = [
                'python', 'generate_reports.py',
                '--excel',
                '--current-module', current_module,
                '--output', output_path
            ]
            
            file_path = output_path
            output_msg = "Generated Excel report"
            
        else:
            return jsonify({"error": f"Unknown report type: {report_type}"}), 400
        
        # Run the command and capture output
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        
        with open(temp_path, 'w') as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env
            )
            
            for line in process.stdout:
                f.write(line)
                f.flush()
            
            process.wait()
        
        # Read the output
        with open(temp_path, 'r') as f:
            output = f.read()
        
        # Check if the file was created
        if not os.path.exists(file_path):
            return jsonify({
                "error": "Failed to generate report",
                "output": output
            }), 500
        
        return jsonify({
            "success": True,
            "message": output_msg,
            "file_path": file_path,
            "output": output
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "output": f"Error: {str(e)}"
        }), 500
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.route('/api/generate-visualization', methods=['POST'])
def generate_visualization():
    """Generate a visualization based on the request."""
    data = request.json
    visualization_type = data.get('visualization_type')
    
    if not visualization_type:
        return jsonify({"error": "Visualization type is required"}), 400
    
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        # Determine the output image path
        image_filename = f"visualization_{visualization_type}_{int(time.time())}.png"
        output_path = os.path.join('static/images', image_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Build the command based on visualization type
        # Load the data files directly
        assessment_data_path = "assets/comptia/25-04-29/classgradebook-4-29-8am.csv"
        resource_time_data_path = "assets/comptia/25-04-29/timeperresource-04-29-8am.csv"
        study_history_data_path = "assets/comptia/25-04-29/classstudyhistory-04-29-8am.csv"
        
        cmd = [
            'python', 'teaching_assistant.py',
            '--visualize',
            '--assessment-data', assessment_data_path,
            '--resource-time-data', resource_time_data_path,
            '--study-history-data', study_history_data_path,
            '--output', output_path
        ]
        
        if visualization_type != 'class_progress':
            cmd.extend(['--visualization-type', visualization_type])
        
        # Run the command and capture output
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()
        
        with open(temp_path, 'w') as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env
            )
            
            for line in process.stdout:
                f.write(line)
                f.flush()
            
            process.wait()
        
        # Read the output
        with open(temp_path, 'r') as f:
            output = f.read()
        
        # Check if the image was created
        if not os.path.exists(output_path):
            return jsonify({
                "error": "Failed to generate visualization",
                "output": output
            }), 500
        
        # Return the URL to the image
        image_url = f"/static/images/{image_filename}"
        
        return jsonify({
            "success": True,
            "message": f"Generated {visualization_type} visualization",
            "image_path": image_filename,
            "image_url": image_url,
            "output": output
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "output": f"Error: {str(e)}"
        }), 500
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def create_templates_directory():
    """Create the templates directory if it doesn't exist."""
    os.makedirs('templates', exist_ok=True)

def main():
    """Run the web application."""
    global chatbot, api_key
    
    if not api_key:
        print("Error: OpenRouter API key is required.")
        print("Set the OPENROUTER_API_KEY environment variable.")
        return
    
    # Default file paths
    assessment_data_path = "assets/comptia/25-04-29/classgradebook-4-29-8am.csv"
    resource_time_data_path = "assets/comptia/25-04-29/timeperresource-04-29-8am.csv"
    study_history_data_path = "assets/comptia/25-04-29/classstudyhistory-04-29-8am.csv"
    
    # Initialize the chatbot
    chatbot = ta_chatbot.TeachingAssistantChatbot(
        api_key, 
        assessment_data_path=assessment_data_path,
        resource_time_data_path=resource_time_data_path,
        study_history_data_path=study_history_data_path
    )
    
    # Create templates directory
    create_templates_directory()
    
    # Create directories for reports and images
    create_directories()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8095)

if __name__ == '__main__':
    main()

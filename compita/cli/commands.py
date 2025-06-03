"""
CLI commands for the Cyber8 report generator.
"""
import argparse
import sys
import os
import shutil
from pathlib import Path

# Add parent directory to path to allow importing from the package
sys.path.append(str(Path(__file__).parent.parent.parent))

def create_parser():
    """Create the command-line argument parser."""
    # Create a parent parser with common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--assets-dir', help='Path to the assets directory (default: assets)')
    parent_parser.add_argument('--output-dir', help='Path to the output directory (default: reports)')
    
    # Create the main parser with subparsers
    parser = argparse.ArgumentParser(description='Cyber8 Report Generator', parents=[parent_parser])
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Generate all reports command
    all_parser = subparsers.add_parser('generate-all', parents=[parent_parser], help='Generate all reports')
    all_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    
    # Flexible module report command
    module_parser = subparsers.add_parser('flexible-module', parents=[parent_parser], help='Generate flexible module report')
    module_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    module_parser.add_argument('--all-modules', nargs='+', help='List of module numbers to include in the overall analysis')
    module_parser.add_argument('--subset-modules', nargs='+', help='List of module numbers to include in the subset analysis')
    module_parser.add_argument('--exclude-modules', nargs='+', help='List of module numbers to exclude from the overall analysis')
    module_parser.add_argument('--output-prefix', help='Prefix for the output files')
    module_parser.add_argument('--count-partial', action='store_true', help='Count partial completions as fully completed')
    
    # Flexible assessment report command
    assessment_parser = subparsers.add_parser('flexible-assessment', parents=[parent_parser], help='Generate flexible assessment report')
    assessment_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    assessment_parser.add_argument('--assessment-types', nargs='+', help='List of assessment types to include')
    assessment_parser.add_argument('--output-prefix', help='Prefix for the output files')
    
    # Flexible grades report command
    grades_parser = subparsers.add_parser('flexible-grades', parents=[parent_parser], help='Generate flexible grades report')
    grades_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    grades_parser.add_argument('--grade-categories', nargs='+', help='List of grade categories to include')
    grades_parser.add_argument('--grade-weights', nargs='+', type=float, help='List of grade weights')
    grades_parser.add_argument('--output-prefix', help='Prefix for the output files')
    
    # Markdown to PDF command
    pdf_parser = subparsers.add_parser('markdown-to-pdf', parents=[parent_parser], help='Convert markdown to PDF')
    pdf_parser.add_argument('--input-dir', required=True, help='Input directory containing markdown files')
    pdf_parser.add_argument('--pdf-output-dir', required=True, help='Output directory for PDF files')
    
    # CSV module report command
    csv_module_parser = subparsers.add_parser('csv-module', parents=[parent_parser], help='Generate CSV report for a specific module')
    csv_module_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    csv_module_parser.add_argument('--module', required=True, type=int, help='Module number to generate the report for')
    csv_module_parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
    
    # CSV student report command
    csv_student_parser = subparsers.add_parser('csv-student', parents=[parent_parser], help='Generate CSV report for a specific student')
    csv_student_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    csv_student_parser.add_argument('--student', required=True, help='Student name to generate the report for')
    
    # CSV class report command
    csv_class_parser = subparsers.add_parser('csv-class', parents=[parent_parser], help='Generate CSV report for the entire class')
    csv_class_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    csv_class_parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
    
    # Excel report command
    excel_parser = subparsers.add_parser('excel-report', parents=[parent_parser], help='Generate Excel report with multiple sheets')
    excel_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    excel_parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
    
    # All CSV reports command
    csv_all_parser = subparsers.add_parser('csv-all', parents=[parent_parser], help='Generate all CSV reports')
    csv_all_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    csv_all_parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
    
    # API server command
    api_parser = subparsers.add_parser('api', parents=[parent_parser], help='Start the API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to (default: 0.0.0.0)')
    api_parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to (default: 8000)')
    api_parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    # Web server command
    web_parser = subparsers.add_parser('web', parents=[parent_parser], help='Start the web interface')
    web_parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to (default: 0.0.0.0)')
    web_parser.add_argument('--port', type=int, default=8080, help='Port to bind the server to (default: 8080)')
    web_parser.add_argument('--api-url', default='http://localhost:8000', help='URL of the API server (default: http://localhost:8000)')
    
    # Full app command (API + Web)
    app_parser = subparsers.add_parser('app', parents=[parent_parser], help='Start both API server and web interface')
    app_parser.add_argument('--api-host', default='0.0.0.0', help='Host to bind the API server to (default: 0.0.0.0)')
    app_parser.add_argument('--api-port', type=int, default=8000, help='Port to bind the API server to (default: 8000)')
    app_parser.add_argument('--web-host', default='0.0.0.0', help='Host to bind the web server to (default: 0.0.0.0)')
    app_parser.add_argument('--web-port', type=int, default=8080, help='Port to bind the web server to (default: 8080)')
    app_parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    return parser

def generate_all(args):
    """
    Generate all reports for the specified date.
    
    Args:
        args: Command line arguments
    """
    print(f"Generating all reports for date: {args.date}")
    
    # Define base directories
    assets_dir = args.assets_dir or 'assets'
    output_dir = args.output_dir or 'reports'
    
    # Step 1: Parse CSV files to JSON
    print("Step 1: Parsing CSV files to JSON...")
    try:
        from compita.parsers.csv_parser import parse_csv
        # Parse CSV files and ensure they're saved with the correct names
        parse_csv(args.date, 'classgradebook', 'gradebook', assets_dir=assets_dir)
        parse_csv(args.date, 'studyhistory', 'study', assets_dir=assets_dir)
        parse_csv(args.date, 'timeperresource', 'resource', assets_dir=assets_dir)
        
        # Create the standardized JSON files in the processed directory
        processed_dir = f"{assets_dir}/processed/{args.date}"
        import os
        import shutil
        import glob
        import re
        
        # Ensure the directory exists
        os.makedirs(processed_dir, exist_ok=True)
        
        # Check if the date-specific directory exists (this is the nested directory we want to avoid)
        date_specific_dir = f"{processed_dir}/{args.date}"
        if os.path.exists(date_specific_dir):
            # If the nested directory exists, move files to the parent directory and remove the nested directory
            for source_name in ["classgradebook.json", "studyhistory.json", "timeperresource.json"]:
                source_file = f"{date_specific_dir}/{source_name}"
                if os.path.exists(source_file):
                    # Move the file to the parent directory
                    target_file = f"{processed_dir}/{source_name}"
                    print(f"Moving {source_file} to {target_file}")
                    shutil.copy2(source_file, target_file)
            
            # Now that we've moved the files, we can remove the nested directory
            # But first check if there are any other files we should keep
            other_files = [f for f in os.listdir(date_specific_dir) 
                          if f not in ["classgradebook.json", "studyhistory.json", "timeperresource.json"]]
            
            if not other_files:
                print(f"Removing redundant nested directory: {date_specific_dir}")
                shutil.rmtree(date_specific_dir)
            else:
                print(f"Not removing {date_specific_dir} as it contains other files: {other_files}")
        
        # Now create the time-date format files based on the original CSV file names
        # Find the original CSV files
        comptia_dir = f"{assets_dir}/comptia/{args.date}"
        if os.path.exists(comptia_dir):
            # Look for CSV files with time-date format
            csv_files = {
                "classgradebook": glob.glob(f"{comptia_dir}/classgradebook-*.csv"),
                "studyhistory": glob.glob(f"{comptia_dir}/classstudyhistory-*.csv"),
                "timeperresource": glob.glob(f"{comptia_dir}/timeperresource-*.csv")
            }
            
            # Create JSON files with time-date format names
            for file_type, files in csv_files.items():
                if files:
                    # Use the most recent file if multiple exist
                    csv_file = sorted(files)[-1]
                    # Extract the time-date part from the CSV filename
                    match = re.search(r'-([\d-]+[ap]m)\.csv$', csv_file)
                    if match:
                        time_date = match.group(1)
                        source_file = f"{processed_dir}/{file_type}.json"
                        target_file = f"{processed_dir}/{file_type}-{time_date}.json"
                        if os.path.exists(source_file):
                            print(f"Creating time-date format file: {target_file}")
                            shutil.copy2(source_file, target_file)
        
        # Also check for files with date-time format and create standardized copies if needed
        for pattern, target_name in [
            ("classgradebook-*.json", "classgradebook.json"),
            ("classstudyhistory-*.json", "studyhistory.json"),  # Note the different pattern name
            ("timeperresource-*.json", "timeperresource.json")
        ]:
            source_files = glob.glob(f"{processed_dir}/{pattern}")
            if source_files:
                # Use the most recent file if multiple exist
                source_file = sorted(source_files)[-1]
                target_file = f"{processed_dir}/{target_name}"
                print(f"Copying {source_file} to {target_file}")
                shutil.copy2(source_file, target_file)
            else:
                print(f"Warning: No source file found matching {pattern} in {processed_dir}")
        
    except ImportError:
        print("\n❌ Error: The pandas library is required for CSV parsing.")
        print("Please install it using: pip3 install pandas")
        print("Or install the complete package with: pip3 install -e .\n")
        return 1
    
    # Step 2: Generate flexible reports
    print("Step 2: Generating flexible reports...")
    try:
        from compita.reports.flexible_module import generate_flexible_module_report
        from compita.reports.flexible_assessment import generate_flexible_assessment_report
        from compita.reports.flexible_grades import generate_flexible_grades_report
        
        # Create the json directory in the reports folder
        json_dir = f"{output_dir}/{args.date}/json"
        os.makedirs(json_dir, exist_ok=True)
        
        # Copy the JSON files to the expected location for the flexible reports
        for source_name, target_name in [
            ("classgradebook.json", "classgradebook.json"),
            ("studyhistory.json", "studyhistory.json"),  # Keep original name
            ("timeperresource.json", "timeperresource.json"),
            ("assessment_data.json", "assessment_data.json"),
            ("study_history_data.json", "study_history_data.json"),
            ("resource_time_data.json", "resource_time_data.json")
        ]:
            source_file = f"{assets_dir}/processed/{args.date}/{source_name}"
            target_file = f"{json_dir}/{target_name}"
            if os.path.exists(source_file):
                print(f"Copying {source_file} to {target_file}")
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)
            else:
                print(f"Warning: Source file {source_file} not found")
        
        # Call the flexible report functions with the correct parameters
        # Check function signatures to determine which parameters to pass
        import inspect
        
        # Generate flexible module report
        module_sig = inspect.signature(generate_flexible_module_report)
        module_kwargs = {}
        if 'assets_dir' in module_sig.parameters:
            module_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in module_sig.parameters:
            module_kwargs['output_dir'] = output_dir
        
        generate_flexible_module_report(args.date, **module_kwargs)
        
        # Generate flexible assessment report
        assessment_sig = inspect.signature(generate_flexible_assessment_report)
        assessment_kwargs = {}
        if 'assets_dir' in assessment_sig.parameters:
            assessment_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in assessment_sig.parameters:
            assessment_kwargs['output_dir'] = output_dir
        
        generate_flexible_assessment_report(args.date, **assessment_kwargs)
        
        # Generate flexible grades report
        grades_sig = inspect.signature(generate_flexible_grades_report)
        grades_kwargs = {}
        if 'assets_dir' in grades_sig.parameters:
            grades_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in grades_sig.parameters:
            grades_kwargs['output_dir'] = output_dir
        
        generate_flexible_grades_report(args.date, **grades_kwargs)
        
    except Exception as e:
        print(f"Error generating flexible reports: {e}")
        import traceback
        traceback.print_exc()
        # Continue with the rest of the process
    
    # Step 3: Generate CSV module reports
    print("Step 3: Generating CSV module reports...")
    try:
        from scripts.generate_reports import main as generate_reports_main
        
        # Save original argv
        original_argv = sys.argv.copy()
        
        # Set up arguments for generate_reports.py
        sys.argv = ['generate_reports.py', 
                    '--date', args.date, 
                    '--all']
        
        if args.assets_dir:
            sys.argv.extend(['--assets-dir', args.assets_dir])
        if args.output_dir:
            sys.argv.extend(['--output-dir', args.output_dir])
        
        generate_reports_main()
        
        # Restore original argv
        sys.argv = original_argv
    except Exception as e:
        print(f"Error generating CSV module reports: {e}")
        import traceback
        traceback.print_exc()
        # Continue with the rest of the process
    
    # Step 4: Collect and combine metrics
    print("Step 4: Collecting and combining metrics...")
    try:
        from compita.collectors.metrics_collector import collect_metrics
        
        # Check function signature to determine which parameters to pass
        metrics_sig = inspect.signature(collect_metrics)
        metrics_kwargs = {}
        if 'assets_dir' in metrics_sig.parameters:
            metrics_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in metrics_sig.parameters:
            metrics_kwargs['output_dir'] = output_dir
        
        collect_metrics(args.date, **metrics_kwargs)
    except Exception as e:
        print(f"Error collecting metrics: {e}")
        import traceback
        traceback.print_exc()
        # Continue with the rest of the process
    
    # Step 5: Generate markdown reports
    print("Step 5: Generating markdown reports...")
    try:
        # Create progress reports directories
        progress_reports_dir = f"{output_dir}/{args.date}/progress_reports"
        student_reports_dir = f"{progress_reports_dir}/student_reports"
        class_summaries_dir = f"{progress_reports_dir}/class_summaries"
        
        os.makedirs(student_reports_dir, exist_ok=True)
        os.makedirs(class_summaries_dir, exist_ok=True)
        
        # Generate student reports
        from compita.reports.report_generator import generate_student_reports

        # Check function signature to determine which parameters to pass
        student_sig = inspect.signature(generate_student_reports)
        student_kwargs = {}
        if 'assets_dir' in student_sig.parameters:
            student_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in student_sig.parameters:
            student_kwargs['output_dir'] = student_reports_dir
        
        generate_student_reports(args.date, **student_kwargs)
        
        # Generate class summary
        from compita.reports.report_generator import generate_class_summary

        # Check function signature to determine which parameters to pass
        class_sig = inspect.signature(generate_class_summary)
        class_kwargs = {}
        if 'assets_dir' in class_sig.parameters:
            class_kwargs['assets_dir'] = assets_dir
        if 'output_dir' in class_sig.parameters:
            class_kwargs['output_dir'] = class_summaries_dir
        
        generate_class_summary(args.date, **class_kwargs)
        
        # Move any student reports from the root reports directory to the correct location
        # This is a temporary fix for reports that might have been generated in the wrong location
        import glob
        root_student_reports = glob.glob(f"reports/student_*.md")
        if root_student_reports:
            print(f"Moving {len(root_student_reports)} student reports from root directory to {student_reports_dir}")
            for report in root_student_reports:
                filename = os.path.basename(report)
                target = os.path.join(student_reports_dir, filename)
                shutil.copy2(report, target)
                os.remove(report)  # Remove the original file after copying
    except Exception as e:
        print(f"Error generating markdown reports: {e}")
        import traceback
        traceback.print_exc()
        # Continue with the rest of the process
    
    # Step 6: Convert markdown to PDF
    print("Step 6: Converting markdown to PDF...")
    try:
        # Create executive reports directory
        executive_reports_dir = f"{output_dir}/{args.date}/executive_reports"
        os.makedirs(executive_reports_dir, exist_ok=True)
        os.makedirs(f"{executive_reports_dir}/student_reports", exist_ok=True)
        os.makedirs(f"{executive_reports_dir}/class_summaries", exist_ok=True)
        
        # Convert student reports
        from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
        
        # Convert student reports
        convert_markdown_to_pdf(
            input_dir=student_reports_dir,
            output_dir=f"{executive_reports_dir}/student_reports"
        )
        
        # Convert class summary
        convert_markdown_to_pdf(
            input_dir=class_summaries_dir,
            output_dir=f"{executive_reports_dir}/class_summaries"
        )
    except Exception as e:
        print(f"Error converting markdown to PDF: {e}")
        import traceback
        traceback.print_exc()
    
    print("Report generation complete!")

def run_command(args=None):
    """Run the specified command."""
    parser = create_parser()
    if args is None:
        args = parser.parse_args()
    
    if args.command == 'generate-all':
        return generate_all(args)
    
    elif args.command == 'flexible-module':
        from compita.reports.flexible_module import generate_flexible_module_report
        return generate_flexible_module_report(
            args.date,
            args.all_modules,
            args.subset_modules,
            args.exclude_modules,
            args.output_prefix,
            args.count_partial
        )
    
    elif args.command == 'flexible-assessment':
        from compita.reports.flexible_assessment import generate_flexible_assessment_report
        return generate_flexible_assessment_report(
            args.date,
            args.assessment_types,
            args.output_prefix
        )
    
    elif args.command == 'flexible-grades':
        from compita.reports.flexible_grades import generate_flexible_grades_report
        return generate_flexible_grades_report(
            args.date,
            args.grade_categories,
            args.grade_weights,
            args.output_prefix
        )
    
    elif args.command == 'markdown-to-pdf':
        from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
        return convert_markdown_to_pdf(args.input_dir, args.pdf_output_dir)
    
    elif args.command in ['csv-module', 'csv-student', 'csv-class', 'excel-report', 'csv-all']:
        from scripts.generate_reports import main as generate_reports_main
        
        # Define base directories
        assets_dir = args.assets_dir or 'assets'
        output_dir = args.output_dir or 'reports'
        
        # Check if the processed data directory exists
        processed_dir = f"{assets_dir}/processed/{args.date}"
        if not os.path.exists(processed_dir):
            print(f"\n❌ Error: The directory '{processed_dir}' does not exist.")
            print(f"This directory is required for generating reports.")
            print(f"Please run the following command first to parse CSV files to JSON:")
            if args.assets_dir:
                print(f"  ./compita-cli generate-all --date {args.date} --assets-dir {args.assets_dir}")
            else:
                print(f"  ./compita-cli generate-all --date {args.date}")
            print()
            return 1
            
        # Check if required JSON files exist
        required_files = [
            f"{processed_dir}/assessment_data.json",
            f"{processed_dir}/resource_time_data.json"
        ]
        missing_files = [f for f in required_files if not os.path.exists(f)]
        if missing_files:
            print(f"\n❌ Error: The following required JSON files are missing:")
            for file in missing_files:
                print(f"  - {file}")
            print(f"\nPlease run the following command first to parse CSV files to JSON:")
            if args.assets_dir:
                print(f"  ./compita-cli generate-all --date {args.date} --assets-dir {args.assets_dir}")
            else:
                print(f"  ./compita-cli generate-all --date {args.date}")
            print()
            return 1
        
        # Save original argv
        original_argv = sys.argv.copy()
        
        # Prepare arguments for the generate_reports.py script
        if args.command == 'csv-module':
            sys.argv = ['generate_reports.py', 
                       '--date', args.date,
                       '--module', str(args.module),
                       '--current-module', str(args.current_module)]
        
        elif args.command == 'csv-student':
            sys.argv = ['generate_reports.py', 
                       '--date', args.date,
                       '--student', args.student]
        
        elif args.command == 'csv-class':
            sys.argv = ['generate_reports.py', 
                       '--date', args.date,
                       '--current-module', str(args.current_module)]
        
        elif args.command == 'excel-report':
            sys.argv = ['generate_reports.py', 
                       '--date', args.date,
                       '--excel',
                       '--current-module', str(args.current_module)]
        
        elif args.command == 'csv-all':
            sys.argv = ['generate_reports.py', 
                       '--date', args.date,
                       '--all',
                       '--current-module', str(args.current_module)]
        
        # Add assets and output directory arguments if provided
        if args.assets_dir:
            sys.argv.extend(['--assets-dir', args.assets_dir])
        if args.output_dir:
            sys.argv.extend(['--output-dir', args.output_dir])
        
        # Run the command
        result = generate_reports_main()
        
        # Restore original argv
        sys.argv = original_argv
        
        return result
    
    elif args.command == 'api':
        try:
            import uvicorn
            from importlib.util import find_spec
            
            # Check if FastAPI is installed
            if find_spec("fastapi") is None:
                print("\n❌ Error: FastAPI is required for the API server.")
                print("Please install it using: uv pip install fastapi uvicorn python-multipart")
                print("Or install the complete package with: uv pip install -e .\n")
                return 1
            
            # Import the API module
            try:
                from compita.src.api.main import app
                print(f"Starting API server at http://{args.host}:{args.port}")
                print(f"API documentation available at http://{args.host}:{args.port}/docs")
                uvicorn.run("compita.src.api.main:app", host=args.host, port=args.port, reload=args.reload)
                return 0
            except ImportError as e:
                print(f"\n❌ Error importing API module: {e}")
                print("Make sure the API module is properly installed.\n")
                return 1
        except ImportError:
            print("\n❌ Error: uvicorn is required for the API server.")
            print("Please install it using: uv pip install uvicorn")
            print("Or install the complete package with: uv pip install -e .\n")
            return 1
    
    elif args.command == 'web':
        try:
            import threading
            import webbrowser
            import time
            import os
            import sys
            from pathlib import Path
            
            # Find the web interface directory
            web_dir = os.path.join(Path(__file__).parent.parent.absolute(), "src", "web")
            
            if not os.path.exists(web_dir):
                print(f"\n❌ Error: Web interface directory not found at {web_dir}")
                return 1
            
            # Try to import Flask
            try:
                from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for
            except ImportError:
                print("\n❌ Error: Flask is required for the web interface.")
                print("Please install it using: uv pip install flask")
                print("Or install the complete package with: uv pip install -e .\n")
                return 1
            
            # Set environment variable for API URL
            os.environ["API_URL"] = args.api_url
            
            # Import the Flask app from the server module
            sys.path.append(web_dir)
            try:
                from server import app
                print(f"Starting web server at http://{args.host}:{args.port}")
                print(f"Web interface is available at http://localhost:{args.port}")
                print("Press Ctrl+C to stop the server")
                
                # Open the web browser after a short delay
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f"http://localhost:{args.port}")
                
                threading.Thread(target=open_browser).start()
                
                # Start the Flask server
                app.run(host=args.host, port=args.port, debug=False)
            except ImportError as e:
                print(f"\n❌ Error importing Flask server module: {e}")
                print("Make sure the server.py file exists in the web directory.\n")
                return 1
            
            return 0
        except Exception as e:
            print(f"\n❌ Error starting web server: {e}")
            return 1
    
    elif args.command == 'app':
        try:
            import multiprocessing
            import subprocess
            import sys
            import os
            import time
            import webbrowser
            
            # Get the path to the compita executable
            compita_path = shutil.which("compita")
            if not compita_path:
                # If not found in PATH, use the current Python executable with the CLI module
                compita_path = sys.executable
                api_cmd = [compita_path, "-m", "compita.cli.main", "api", 
                          "--host", args.api_host, "--port", str(args.api_port)]
            else:
                # Use the compita executable directly
                api_cmd = [compita_path, "api", "--host", args.api_host, 
                          "--port", str(args.api_port)]
            
            if args.reload:
                api_cmd.append("--reload")
                
            print(f"Starting API server with command: {' '.join(api_cmd)}")
            api_process = subprocess.Popen(api_cmd)
            
            # Give the API server a moment to start
            time.sleep(2)
            
            # Start the web server in the current process
            if compita_path == sys.executable:
                web_cmd = [compita_path, "-m", "compita.cli.main", "web", 
                          "--host", args.web_host, "--port", str(args.web_port),
                          "--api-url", f"http://{args.api_host}:{args.api_port}"]
            else:
                web_cmd = [compita_path, "web", "--host", args.web_host, 
                          "--port", str(args.web_port),
                          "--api-url", f"http://{args.api_host}:{args.api_port}"]
            
            web_process = subprocess.Popen(web_cmd)
            
            print(f"Cyber8 app started:")
            print(f"API server: http://{args.api_host}:{args.api_port}")
            print(f"Web interface: http://{args.web_host}:{args.web_port}")
            print("Press Ctrl+C to stop both servers")
            
            # Note: The web server will open a browser automatically
            # We don't need to open a second browser tab here
            
            try:
                # Wait for keyboard interrupt
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping servers...")
                api_process.terminate()
                web_process.terminate()
                print("Servers stopped")
            
            return 0
        except Exception as e:
            print(f"\n❌ Error starting app: {e}")
            return 1
    
    else:
        print("No command specified. Use --help for usage information.")
        return 1

if __name__ == '__main__':
    sys.exit(run_command())

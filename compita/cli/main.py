"""
Main CLI entry point for the Cyber8 report generator.
"""
import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path to allow importing from the package
sys.path.append(str(Path(__file__).parent.parent.parent))

from compita.utils.logger import setup_logger
from compita.utils.config import config

logger = setup_logger('cli')

def parse_args():
    """Parse command line arguments."""
    # Create a parent parser with common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--assets-dir', help='Path to the assets directory (default: assets)')
    parent_parser.add_argument('--output-dir', help='Path to the output directory (default: reports)')
    
    # Main parser
    parser = argparse.ArgumentParser(description='Cyber8 Report Generator', parents=[parent_parser])
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
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
    assessment_parser.add_argument('--date-range', help='Date range for overall analysis')
    assessment_parser.add_argument('--subset-range', help='Date range for subset analysis')
    assessment_parser.add_argument('--output-prefix', help='Prefix for the output files')
    assessment_parser.add_argument('--min-study-threshold', type=int, help='Minimum study time in seconds')
    
    # Flexible grades report command
    grades_parser = subparsers.add_parser('flexible-grades', parents=[parent_parser], help='Generate flexible grades report')
    grades_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    grades_parser.add_argument('--all-modules', nargs='+', help='List of module numbers to include in the overall analysis')
    grades_parser.add_argument('--subset-modules', nargs='+', help='List of module numbers to include in the subset analysis')
    grades_parser.add_argument('--exclude-modules', nargs='+', help='List of module numbers to exclude from the analysis')
    grades_parser.add_argument('--assessment-types', nargs='+', help='List of assessment types to include')
    grades_parser.add_argument('--output-prefix', help='Prefix for the output files')
    grades_parser.add_argument('--min-grade-threshold', type=float, help='Minimum grade to count an assessment as passed')
    grades_parser.add_argument('--count-incomplete', action='store_true', help='Count assessments with 0.0 completion in averages')
    
    # Markdown to PDF command
    pdf_parser = subparsers.add_parser('markdown-to-pdf', parents=[parent_parser], help='Convert markdown to PDF')
    pdf_parser.add_argument('--input-dir', required=True, help='Input directory containing markdown files')
    pdf_parser.add_argument('--pdf-output-dir', required=True, help='Output directory for PDF files')
    
    # CSV module report command
    csv_module_parser = subparsers.add_parser('csv-module', parents=[parent_parser], help='Generate CSV report for a specific module')
    csv_module_parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    csv_module_parser.add_argument('--module', required=True, type=int, help='Module number to generate the report for')
    
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
    
    # Add current-module argument to csv-module parser
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
    
    return parser.parse_args()

def generate_all(args=None):
    """Generate all reports."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate all reports')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        args = parser.parse_args()
    
    logger.info(f"Generating all reports for date: {args.date}")
    
    # Ensure directories exist
    config.ensure_directories(args.date)
    
    # Import here to avoid circular imports
    from compita.parsers.csv_parser import parse_csv
    from compita.reports.flexible_module import generate_flexible_module_report
    from compita.reports.flexible_assessment import generate_flexible_assessment_report
    from compita.reports.flexible_grades import generate_flexible_grades_report
    from compita.reports.report_generator import generate_reports, generate_class_summary
    from compita.collectors.metrics_collector import collect_metrics
    from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
    
    # Step 1: Parse CSV files to JSON
    logger.info("Step 1: Parsing CSV files to JSON...")
    parse_csv(args.date, 'classgradebook', 'gradebook')
    parse_csv(args.date, 'studyhistory', 'study')
    parse_csv(args.date, 'timeperresource', 'resource')
    
    # Step 2: Generate flexible reports
    logger.info("Step 2: Generating flexible reports...")
    generate_flexible_module_report(args.date)
    generate_flexible_assessment_report(args.date)
    generate_flexible_grades_report(args.date)
    
    # Step 3: Generate CSV module reports
    logger.info("Step 3: Generating CSV module reports...")
    # Call the generate_reports.py functionality
    from scripts.generate_reports import main as generate_reports_main
    original_argv = sys.argv.copy()
    sys.argv = ['generate_reports.py', '--date', args.date, '--all']
    generate_reports_main()
    sys.argv = original_argv
    
    # Step 4: Collect and combine metrics
    logger.info("Step 4: Collecting and combining metrics...")
    collect_metrics(args.date)
    
    # Step 5: Generate markdown reports
    logger.info("Step 5: Generating markdown reports...")
    generate_reports(args.date)
    generate_class_summary(args.date)
    
    # Step 6: Convert markdown to PDF
    logger.info("Step 6: Converting markdown to PDF...")
    student_reports_dir = config.get_reports_path(args.date, 'student_reports')
    class_summaries_dir = config.get_reports_path(args.date, 'class_summaries')
    executive_reports_dir = config.get_reports_path(args.date, 'executive')
    
    convert_markdown_to_pdf(student_reports_dir, executive_reports_dir)
    convert_markdown_to_pdf(class_summaries_dir, executive_reports_dir)
    
    logger.info("Report generation complete!")
    return 0

def flexible_module(args=None):
    """Generate flexible module report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate flexible module report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--all-modules', nargs='+', help='List of module numbers to include in the overall analysis')
        parser.add_argument('--subset-modules', nargs='+', help='List of module numbers to include in the subset analysis')
        parser.add_argument('--exclude-modules', nargs='+', help='List of module numbers to exclude from the overall analysis')
        parser.add_argument('--output-prefix', help='Prefix for the output files')
        parser.add_argument('--count-partial', action='store_true', help='Count partial completions as fully completed')
        args = parser.parse_args()
    
    logger.info(f"Generating flexible module report for date: {args.date}")
    
    # Import here to avoid circular imports
    from compita.reports.flexible_module import generate_flexible_module_report
    
    # Generate flexible module report
    generate_flexible_module_report(
        args.date,
        args.all_modules,
        args.subset_modules,
        args.exclude_modules,
        args.output_prefix,
        args.count_partial
    )
    
    return 0

def flexible_assessment(args=None):
    """Generate flexible assessment report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate flexible assessment report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--date-range', help='Date range for overall analysis')
        parser.add_argument('--subset-range', help='Date range for subset analysis')
        parser.add_argument('--output-prefix', help='Prefix for the output files')
        parser.add_argument('--min-study-threshold', type=int, help='Minimum study time in seconds')
        args = parser.parse_args()
    
    logger.info(f"Generating flexible assessment report for date: {args.date}")
    
    # Import here to avoid circular imports
    from compita.reports.flexible_assessment import generate_flexible_assessment_report
    
    # Generate flexible assessment report
    generate_flexible_assessment_report(
        args.date,
        args.date_range,
        args.subset_range,
        args.output_prefix,
        args.min_study_threshold
    )
    
    return 0

def flexible_grades(args=None):
    """Generate flexible grades report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate flexible grades report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--all-modules', nargs='+', help='List of module numbers to include in the overall analysis')
        parser.add_argument('--subset-modules', nargs='+', help='List of module numbers to include in the subset analysis')
        parser.add_argument('--exclude-modules', nargs='+', help='List of module numbers to exclude from the analysis')
        parser.add_argument('--assessment-types', nargs='+', help='List of assessment types to include')
        parser.add_argument('--output-prefix', help='Prefix for the output files')
        parser.add_argument('--min-grade-threshold', type=float, help='Minimum grade to count an assessment as passed')
        parser.add_argument('--count-incomplete', action='store_true', help='Count assessments with 0.0 completion in averages')
        args = parser.parse_args()
    
    logger.info(f"Generating flexible grades report for date: {args.date}")
    
    # Import here to avoid circular imports
    from compita.reports.flexible_grades import generate_flexible_grades_report
    
    # Generate flexible grades report
    generate_flexible_grades_report(
        args.date,
        args.all_modules,
        args.subset_modules,
        args.exclude_modules,
        args.assessment_types,
        args.output_prefix,
        args.min_grade_threshold,
        args.count_incomplete
    )
    
    return 0

def markdown_to_pdf(args=None):
    """Convert markdown to PDF."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Convert markdown to PDF')
        parser.add_argument('--input-dir', required=True, help='Input directory containing markdown files')
        parser.add_argument('--pdf-output-dir', required=True, help='Output directory for PDF files')
        args = parser.parse_args()
    
    # Determine the output directory (handle both parameter names for backward compatibility)
    output_dir = args.pdf_output_dir if hasattr(args, 'pdf_output_dir') else args.output_dir
    
    logger.info(f"Converting markdown to PDF from {args.input_dir} to {output_dir}")
    
    # Import here to avoid circular imports
    from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
    
    # Convert markdown to PDF
    convert_markdown_to_pdf(args.input_dir, output_dir)
    
    return 0

def csv_module(args=None):
    """Generate CSV module report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate CSV module report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--module', required=True, type=int, help='Module number to generate the report for')
        parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
        args = parser.parse_args()
    
    logger.info(f"Generating CSV module report for module {args.module}")
    
    # Import here to avoid circular imports
    from scripts.generate_reports import main as generate_reports_main
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Set argv for generate_reports.py
    sys.argv = ['generate_reports.py', 
               '--date', args.date,
               '--module', str(args.module),
               '--current-module', str(args.current_module)]
    
    # Run generate_reports.py
    result = generate_reports_main()
    
    # Restore original argv
    sys.argv = original_argv
    
    return result

def csv_student(args=None):
    """Generate CSV student report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate CSV student report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--student', required=True, help='Student name to generate the report for')
        args = parser.parse_args()
    
    logger.info(f"Generating CSV student report for {args.student}")
    
    # Import here to avoid circular imports
    from scripts.generate_reports import main as generate_reports_main
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Set argv for generate_reports.py
    sys.argv = ['generate_reports.py', 
               '--date', args.date,
               '--student', args.student]
    
    # Run generate_reports.py
    result = generate_reports_main()
    
    # Restore original argv
    sys.argv = original_argv
    
    return result

def csv_class(args=None):
    """Generate CSV class report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate CSV class report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
        args = parser.parse_args()
    
    logger.info(f"Generating CSV class report")
    
    # Import here to avoid circular imports
    from scripts.generate_reports import main as generate_reports_main
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Set argv for generate_reports.py
    sys.argv = ['generate_reports.py', 
               '--date', args.date,
               '--current-module', str(args.current_module)]
    
    # Run generate_reports.py
    result = generate_reports_main()
    
    # Restore original argv
    sys.argv = original_argv
    
    return result

def excel_report(args=None):
    """Generate Excel report."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate Excel report')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
        args = parser.parse_args()
    
    logger.info(f"Generating Excel report")
    
    # Import here to avoid circular imports
    from scripts.generate_reports import main as generate_reports_main
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Set argv for generate_reports.py
    sys.argv = ['generate_reports.py', 
               '--date', args.date,
               '--excel',
               '--current-module', str(args.current_module)]
    
    # Run generate_reports.py
    result = generate_reports_main()
    
    # Restore original argv
    sys.argv = original_argv
    
    return result

def csv_all(args=None):
    """Generate all CSV reports."""
    if args is None:
        # If called as an entry point, parse args
        parser = argparse.ArgumentParser(description='Generate all CSV reports')
        parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
        parser.add_argument('--current-module', type=int, default=7, help='Current module being taught')
        args = parser.parse_args()
    
    logger.info(f"Generating all CSV reports")
    
    # Import here to avoid circular imports
    from scripts.generate_reports import main as generate_reports_main
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Set argv for generate_reports.py
    sys.argv = ['generate_reports.py', 
               '--date', args.date,
               '--all',
               '--current-module', str(args.current_module)]
    
    # Run generate_reports.py
    result = generate_reports_main()
    
    # Restore original argv
    sys.argv = original_argv
    
    return result

def run_interactive():
    """Run the interactive CLI."""
    from compita.cli.interactive import main as interactive_main
    return interactive_main()

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Check if interactive mode is requested
    if hasattr(args, 'interactive') and args.interactive:
        return run_interactive()
    
    if args.command == 'generate-all':
        return generate_all(args)
    elif args.command == 'flexible-module':
        return flexible_module(args)
    elif args.command == 'flexible-assessment':
        return flexible_assessment(args)
    elif args.command == 'flexible-grades':
        return flexible_grades(args)
    elif args.command == 'markdown-to-pdf':
        return markdown_to_pdf(args)
    elif args.command == 'csv-module':
        return csv_module(args)
    elif args.command == 'csv-student':
        return csv_student(args)
    elif args.command == 'csv-class':
        return csv_class(args)
    elif args.command == 'excel-report':
        return excel_report(args)
    elif args.command == 'csv-all':
        return csv_all(args)
    elif args.command in ['api', 'web', 'app']:
        # Import and run commands from the commands module
        from compita.cli.commands import run_command
        return run_command(args)
    else:
        print("No command specified. Use --help for usage information.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Cyber8 Report Generator API

This module provides a FastAPI interface for the Cyber8 Report Generator,
allowing users to generate reports, parse CSV files, and access metrics
through a RESTful API.
"""

import os
import re
import json
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import Cyber8 modules
from compita.parsers.csv_parser import parse_csv
from compita.collectors.metrics_collector import collect_metrics
from compita.reports.report_generator import generate_student_reports, generate_class_summary
from compita.reports.flexible_module import generate_flexible_module_report
from compita.reports.flexible_assessment import generate_flexible_assessment_report
from compita.reports.flexible_grades import generate_flexible_grades_report
from compita.converters.markdown_to_pdf import convert_markdown_to_pdf

# Create FastAPI application
app = FastAPI(
    title="Cyber8 Report Generator API",
    description="API for generating student and class reports from Cyber8 data",
    version="1.0.0"
)

# Get environment variables with defaults
def get_env_var(name, default):
    return os.environ.get(name, default)

# Configure environment variables
ENVIRONMENT = get_env_var("ENVIRONMENT", "development")
DEBUG = get_env_var("DEBUG", "false").lower() == "true"
ASSETS_DIR = get_env_var("ASSETS_DIR", "assets")
REPORTS_DIR = get_env_var("REPORTS_DIR", "reports")
ENABLE_PERSISTENCE = get_env_var("ENABLE_PERSISTENCE", "true").lower() == "true"

# Create directories if they don't exist
if ENABLE_PERSISTENCE:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

# Configure CORS
allowed_origins = get_env_var("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in allowed_origins.split(",")]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request/response validation
class DateRequest(BaseModel):
    date: str  # YY-MM-DD format

class ParseCSVRequest(BaseModel):
    date: str
    file_type: str
    parser_type: str
    assets_dir: str = "assets"

class FlexibleModuleRequest(BaseModel):
    date: str
    all_modules: Optional[List[int]] = None
    subset_modules: Optional[List[int]] = None
    exclude_modules: Optional[List[int]] = None
    output_prefix: Optional[str] = None
    count_partial: bool = False
    assets_dir: str = "assets"
    output_dir: str = None  # Set to None to use the default path: reports/{date}/flexible_reports

class FlexibleAssessmentRequest(BaseModel):
    date: str
    assessment_types: Optional[List[str]] = None
    output_prefix: Optional[str] = None
    modules: Optional[List[int]] = None
    assets_dir: str = "assets"
    output_dir: str = "reports"

class FlexibleGradesRequest(BaseModel):
    date: str
    grade_categories: Optional[List[str]] = None
    grade_weights: Optional[Dict[str, float]] = None
    output_prefix: Optional[str] = None
    modules: Optional[List[int]] = None
    assets_dir: str = "assets"
    output_dir: str = "reports"

class StudentReportsRequest(BaseModel):
    date: str
    students: Optional[List[str]] = None
    output_dir: Optional[str] = None
    assets_dir: str = "assets"

class ClassSummaryRequest(BaseModel):
    date: str
    output_dir: Optional[str] = None
    assets_dir: str = "assets"

class MarkdownToPDFRequest(BaseModel):
    input_dir: str
    output_dir: str

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Dictionary to store background task status
task_status = {}

# Helper function to validate date format
def validate_date(date: str) -> bool:
    """Validate that the date is in YY-MM-DD format"""
    try:
        datetime.strptime(date, "%y-%m-%d")
        return True
    except ValueError:
        return False

# Helper function to update task status
def update_task_status(task_id: str, status: str, message: str, result: Any = None):
    """Update the status of a background task"""
    task_status[task_id] = {
        "status": status,
        "message": message,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }

# API Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Cyber8 Report Generator API",
        "version": "1.0.0",
        "description": "API for generating student and class reports from Cyber8 data"
    }

@app.get("/api/v1/status/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a background task"""
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return task_status[task_id]

@app.post("/api/v1/parse-csv", response_model=TaskResponse)
async def api_parse_csv(request: ParseCSVRequest, background_tasks: BackgroundTasks):
    """Parse CSV files to JSON"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"parse_csv_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_csv():
        try:
            update_task_status(task_id, "running", f"Parsing {request.file_type} CSV files for {request.date}")
            result = parse_csv(
                request.date,
                request.file_type,
                request.parser_type,
                assets_dir=request.assets_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully parsed {request.file_type} CSV files for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error parsing CSV files: {str(e)}")
    
    background_tasks.add_task(process_csv)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started parsing {request.file_type} CSV files for {request.date}"
    }

@app.post("/api/v1/collect-metrics", response_model=TaskResponse)
async def api_collect_metrics(request: DateRequest, background_tasks: BackgroundTasks):
    """Collect and combine metrics from all data sources"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"collect_metrics_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_metrics():
        try:
            update_task_status(task_id, "running", f"Collecting metrics for {request.date}")
            result = collect_metrics(request.date)
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully collected metrics for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error collecting metrics: {str(e)}")
    
    background_tasks.add_task(process_metrics)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started collecting metrics for {request.date}"
    }

@app.post("/api/v1/flexible-module", response_model=TaskResponse)
async def api_flexible_module(request: FlexibleModuleRequest, background_tasks: BackgroundTasks):
    """Generate flexible module report"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"flexible_module_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_report():
        try:
            update_task_status(task_id, "running", f"Generating flexible module report for {request.date}")
            result = generate_flexible_module_report(
                request.date,
                request.all_modules,
                request.subset_modules,
                request.exclude_modules,
                request.output_prefix,
                request.count_partial,
                assets_dir=request.assets_dir,
                output_dir=request.output_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated flexible module report for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error generating flexible module report: {str(e)}")
    
    background_tasks.add_task(process_report)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating flexible module report for {request.date}"
    }

@app.post("/api/v1/flexible-assessment", response_model=TaskResponse)
async def api_flexible_assessment(request: FlexibleAssessmentRequest, background_tasks: BackgroundTasks):
    """Generate flexible assessment report"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"flexible_assessment_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_report():
        try:
            update_task_status(task_id, "running", f"Generating flexible assessment report for {request.date}")
            result = generate_flexible_assessment_report(
                request.date,
                request.assessment_types,
                request.output_prefix,
                request.modules,
                assets_dir=request.assets_dir,
                output_dir=request.output_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated flexible assessment report for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error generating flexible assessment report: {str(e)}")
    
    background_tasks.add_task(process_report)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating flexible assessment report for {request.date}"
    }

@app.post("/api/v1/flexible-grades", response_model=TaskResponse)
async def api_flexible_grades(request: FlexibleGradesRequest, background_tasks: BackgroundTasks):
    """Generate flexible grades report"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"flexible_grades_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_report():
        try:
            update_task_status(task_id, "running", f"Generating flexible grades report for {request.date}")
            result = generate_flexible_grades_report(
                request.date,
                request.grade_categories,
                request.grade_weights,
                request.output_prefix,
                request.modules,
                assets_dir=request.assets_dir,
                output_dir=request.output_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated flexible grades report for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error generating flexible grades report: {str(e)}")
    
    background_tasks.add_task(process_report)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating flexible grades report for {request.date}"
    }

@app.post("/api/v1/student-reports", response_model=TaskResponse)
async def api_student_reports(request: StudentReportsRequest, background_tasks: BackgroundTasks):
    """Generate student reports"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"student_reports_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_reports():
        try:
            update_task_status(task_id, "running", f"Generating student reports for {request.date}")
            result = generate_student_reports(
                request.date,
                output_dir=request.output_dir,
                students=request.students
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated student reports for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error generating student reports: {str(e)}")
    
    background_tasks.add_task(process_reports)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating student reports for {request.date}"
    }

@app.post("/api/v1/class-summary", response_model=TaskResponse)
async def api_class_summary(request: ClassSummaryRequest, background_tasks: BackgroundTasks):
    """Generate class summary report"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"class_summary_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_report():
        try:
            update_task_status(task_id, "running", f"Generating class summary for {request.date}")
            result = generate_class_summary(
                request.date,
                output_dir=request.output_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated class summary for {request.date}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error generating class summary: {str(e)}")
    
    background_tasks.add_task(process_report)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating class summary for {request.date}"
    }

@app.post("/api/v1/markdown-to-pdf", response_model=TaskResponse)
async def api_markdown_to_pdf(request: MarkdownToPDFRequest, background_tasks: BackgroundTasks):
    """Convert markdown files to PDF"""
    task_id = f"markdown_to_pdf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_conversion():
        try:
            update_task_status(task_id, "running", f"Converting markdown to PDF")
            result = convert_markdown_to_pdf(
                request.input_dir,
                request.output_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully converted markdown to PDF",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error converting markdown to PDF: {str(e)}")
    
    background_tasks.add_task(process_conversion)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started converting markdown to PDF"
    }

@app.post("/api/v1/upload-csv")
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    date: str = Form(...),
    file_type: str = Form(...),
    parser_type: str = Form(...),
    assets_dir: str = Form("assets")
):
    """Upload and parse a CSV file"""
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    # Create directory structure
    comptia_dir = os.path.join(assets_dir, "comptia", date)
    os.makedirs(comptia_dir, exist_ok=True)
    
    # Generate a filename with timestamp
    timestamp = datetime.now().strftime("%m-%d-%I%p")
    filename = f"{file_type}-{timestamp}.csv"
    file_path = os.path.join(comptia_dir, filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Parse the CSV file in the background
    task_id = f"upload_csv_{date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_uploaded_csv():
        try:
            update_task_status(task_id, "running", f"Parsing uploaded CSV file: {filename}")
            result = parse_csv(
                date,
                file_type,
                parser_type,
                assets_dir=assets_dir
            )
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully parsed uploaded CSV file: {filename}",
                result
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error parsing uploaded CSV file: {str(e)}")
    
    background_tasks.add_task(process_uploaded_csv)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started parsing uploaded CSV file: {filename}",
        "filename": filename,
        "file_path": file_path
    }

@app.post("/api/v1/generate-all", response_model=TaskResponse)
async def api_generate_all(request: DateRequest, background_tasks: BackgroundTasks):
    """Generate all reports for a specific date"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"generate_all_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def copy_processed_files(date_folder):
        """Copy processed JSON files to the expected locations and fix directory structure"""
        # Define directories
        processed_dir = f"assets/processed/{date_folder}"
        duplicated_dir = f"assets/processed/{date_folder}/{date_folder}"
        reports_json_dir = f"reports/{date_folder}/json"
        
        # Create the reports/json directory if it doesn't exist
        os.makedirs(reports_json_dir, exist_ok=True)
        
        # First, check if the nested directory exists and move files to the parent directory
        if os.path.exists(duplicated_dir):
            for filename in ["classgradebook.json", "studyhistory.json", "timeperresource.json"]:
                source_path = os.path.join(duplicated_dir, filename)
                if os.path.exists(source_path):
                    # Move the file to the parent directory
                    target_path = os.path.join(processed_dir, filename)
                    print(f"Moving {source_path} to {target_path}")
                    shutil.copy2(source_path, target_path)
            
            # Check if there are any other files we should keep before removing the nested directory
            other_files = [f for f in os.listdir(duplicated_dir) 
                          if f not in ["classgradebook.json", "studyhistory.json", "timeperresource.json"]]
            
            if not other_files:
                print(f"Removing redundant nested directory: {duplicated_dir}")
                try:
                    shutil.rmtree(duplicated_dir)
                except Exception as e:
                    print(f"Warning: Could not remove directory {duplicated_dir}: {e}")
            else:
                print(f"Not removing {duplicated_dir} as it contains other files: {other_files}")
        
        # Copy all necessary files to the reports/json directory
        for source_name, target_name in [
            ("classgradebook.json", "classgradebook.json"),
            ("studyhistory.json", "studyhistory.json"),
            ("timeperresource.json", "timeperresource.json"),
            ("assessment_data.json", "assessment_data.json"),
            ("study_history_data.json", "study_history_data.json"),
            ("resource_time_data.json", "resource_time_data.json")
        ]:
            source_path = os.path.join(processed_dir, source_name)
            target_path = os.path.join(reports_json_dir, target_name)
            if os.path.exists(source_path):
                print(f"Copying {source_path} to {target_path}")
                shutil.copy2(source_path, target_path)
            else:
                print(f"Warning: Source file {source_path} not found")

    def process_all():
        try:
            update_task_status(task_id, "running", f"Generating all reports for {request.date}")
            
            # Step 1: Parse CSV files to JSON
            update_task_status(task_id, "running", f"Step 1: Parsing CSV files to JSON")
            parse_csv(request.date, 'classgradebook', 'gradebook')
            parse_csv(request.date, 'studyhistory', 'study')
            parse_csv(request.date, 'timeperresource', 'resource')
            
            # Step 1.5: Fix directory structure and copy processed files to the expected locations
            update_task_status(task_id, "running", f"Step 1.5: Fixing directory structure and copying processed files")
            copy_processed_files(request.date)
            
            # Step 2: Generate flexible reports
            update_task_status(task_id, "running", f"Step 2: Generating flexible reports")
            generate_flexible_module_report(request.date)
            generate_flexible_assessment_report(request.date)
            generate_flexible_grades_report(request.date)
            
            # Step 3: Collect metrics
            update_task_status(task_id, "running", f"Step 3: Collecting metrics")
            metrics_path = collect_metrics(request.date)
            
            # Step 4: Generate markdown reports
            update_task_status(task_id, "running", f"Step 4: Generating markdown reports")
            student_reports_dir = f"reports/{request.date}/progress_reports/student_reports"
            class_summaries_dir = f"reports/{request.date}/progress_reports/class_summaries"
            
            os.makedirs(student_reports_dir, exist_ok=True)
            os.makedirs(class_summaries_dir, exist_ok=True)
            
            student_reports = generate_student_reports(request.date, output_dir=student_reports_dir)
            class_summary = generate_class_summary(request.date, output_dir=class_summaries_dir)
            
            # Step 5: Convert markdown to PDF
            update_task_status(task_id, "running", f"Step 5: Converting markdown to PDF")
            executive_reports_dir = f"reports/{request.date}/executive_reports"
            os.makedirs(f"{executive_reports_dir}/student_reports", exist_ok=True)
            os.makedirs(f"{executive_reports_dir}/class_summaries", exist_ok=True)
            
            convert_markdown_to_pdf(
                input_dir=student_reports_dir,
                output_dir=f"{executive_reports_dir}/student_reports"
            )
            
            convert_markdown_to_pdf(
                input_dir=class_summaries_dir,
                output_dir=f"{executive_reports_dir}/class_summaries"
            )
            
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully generated all reports for {request.date}",
                {
                    "metrics_path": metrics_path,
                    "student_reports": student_reports,
                    "class_summary": class_summary,
                    "pdf_output_dir": executive_reports_dir
                }
            )
        except Exception as e:
            import traceback
            update_task_status(
                task_id, 
                "failed", 
                f"Error generating all reports: {str(e)}\n{traceback.format_exc()}"
            )
    
    background_tasks.add_task(process_all)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started generating all reports for {request.date}"
    }

@app.get("/api/v1/available-dates")
async def get_available_dates(assets_dir: str = "assets"):
    """Get a list of available date folders"""
    comptia_dir = os.path.join(assets_dir, "comptia")
    if not os.path.exists(comptia_dir):
        return {"dates": []}
    
    date_pattern = re.compile(r'^\\d{2}-\\d{2}-\\d{2}$')
    dates = []
    
    for item in os.listdir(comptia_dir):
        item_path = os.path.join(comptia_dir, item)
        if os.path.isdir(item_path) and date_pattern.match(item):
            dates.append(item)
    
    # Sort dates in descending order (newest first)
    dates.sort(reverse=True)
    
    return {"dates": dates}

@app.get("/api/v1/available-reports/{date}")
async def get_available_reports(date: str):
    """Get a list of available reports for a specific date"""
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    # Define report directories to check
    report_dirs = {
        "student_markdown": f"reports/{date}/progress_reports/student_reports",
        "class_markdown": f"reports/{date}/progress_reports/class_summaries",
        "student_pdf": f"reports/{date}/executive_reports/student_reports",
        "class_pdf": f"reports/{date}/executive_reports/class_summaries",
        "flexible": f"reports/{date}/flexible_reports",
        "metrics": f"reports/{date}/metrics"
    }
    
    reports = []
    
    # Check each directory for available reports
    for report_type, dir_path in report_dirs.items():
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    # Get file extension
                    _, ext = os.path.splitext(filename)
                    ext = ext.lstrip('.')
                    
                    # Create a report object
                    reports.append({
                        "filename": filename,
                        "path": file_path,
                        "type": ext,
                        "report_type": report_type,
                        "size": os.path.getsize(file_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
    
    return {"reports": reports}

@app.get("/api/v1/download-report/{date}/{report_type}/{filename}")
async def download_report(date: str, report_type: str, filename: str):
    """Download a generated report file"""
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    # Map report_type to directory
    report_dir_map = {
        "student_markdown": f"reports/{date}/progress_reports/student_reports",
        "class_markdown": f"reports/{date}/progress_reports/class_summaries",
        "student_pdf": f"reports/{date}/executive_reports/student_reports",
        "class_pdf": f"reports/{date}/executive_reports/class_summaries",
        "flexible_module": f"reports/{date}/flexible_reports",
        "flexible_assessment": f"reports/{date}/flexible_reports",
        "flexible_grades": f"reports/{date}/flexible_reports",
        "metrics": f"reports/{date}/metrics"
    }
    
    if report_type not in report_dir_map:
        raise HTTPException(status_code=400, detail=f"Invalid report type: {report_type}")
    
    file_path = os.path.join(report_dir_map[report_type], filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    return FileResponse(file_path)

# Setup Project models
class SetupProjectRequest(BaseModel):
    date: str
    class_name: Optional[str] = "Cyber8 Class"
    current_module: int
    required_files: List[str]

@app.post("/api/v1/setup-project", response_model=TaskResponse)
async def setup_project(request: SetupProjectRequest, background_tasks: BackgroundTasks):
    """Setup a new project with the proper folder structure"""
    if not validate_date(request.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    task_id = f"setup_project_{request.date}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def process_setup():
        try:
            update_task_status(task_id, "running", f"Setting up project for {request.date}")
            
            # Create the necessary directories
            assets_dir = f"assets/comptia/{request.date}"
            reports_dir = f"reports/{request.date}"
            
            # Create directories if they don't exist
            os.makedirs(assets_dir, exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "progress_reports/student_reports"), exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "progress_reports/class_summaries"), exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "executive_reports/student_reports"), exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "executive_reports/class_summaries"), exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "flexible_reports"), exist_ok=True)
            os.makedirs(os.path.join(reports_dir, "metrics"), exist_ok=True)
            
            # Create a class info file
            class_info = {
                "class_name": request.class_name,
                "current_module": request.current_module,
                "date": request.date,
                "required_files": request.required_files
            }
            
            with open(os.path.join(assets_dir, "class_info.json"), "w") as f:
                json.dump(class_info, f, indent=2)
            
            # Generate a directory structure string
            structure = generate_directory_structure(request.date)
            
            update_task_status(
                task_id, 
                "completed", 
                f"Successfully set up project for {request.date}",
                {"structure": structure}
            )
        except Exception as e:
            update_task_status(task_id, "failed", f"Error setting up project: {str(e)}")
    
    background_tasks.add_task(process_setup)
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": f"Started setting up project for {request.date}"
    }

@app.get("/api/v1/validate-project/{date}")
async def validate_project(date: str):
    """Validate an existing project structure"""
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YY-MM-DD")
    
    # Check if the project exists
    assets_dir = f"assets/comptia/{date}"
    reports_dir = f"reports/{date}"
    
    if not os.path.exists(assets_dir):
        return {
            "status": "warning",
            "message": f"Assets directory for {date} does not exist",
            "structure": f"Missing: {assets_dir}"
        }
    
    # Check for required directories
    missing_dirs = []
    required_dirs = [
        os.path.join(reports_dir, "progress_reports/student_reports"),
        os.path.join(reports_dir, "progress_reports/class_summaries"),
        os.path.join(reports_dir, "executive_reports/student_reports"),
        os.path.join(reports_dir, "executive_reports/class_summaries"),
        os.path.join(reports_dir, "flexible_reports"),
        os.path.join(reports_dir, "metrics")
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    # Check for class info file (optional)
    class_info_path = os.path.join(assets_dir, "class_info.json")
    class_info_exists = os.path.exists(class_info_path)
    
    # Generate structure
    structure = generate_directory_structure(date)
    
    if missing_dirs:
        return {
            "status": "incomplete",
            "message": f"Project structure for {date} is incomplete. Missing {len(missing_dirs)} directories",
            "structure": structure
        }
        
    # Note: We don't check for class_info.json anymore as it's optional
    
    return {
        "status": "valid",
        "message": f"Project structure for {date} is valid",
        "structure": structure
    }

def generate_directory_structure(date: str) -> str:
    """Generate a string representation of the directory structure"""
    structure = f"Project Structure for {date}\n"
    structure += "├── assets/\n"
    structure += f"│   └── comptia/{date}/\n"
    
    # Check if class_info.json exists
    class_info_path = f"assets/comptia/{date}/class_info.json"
    if os.path.exists(class_info_path):
        structure += "│       └── class_info.json\n"
        
        # Read class info to show required files
        try:
            with open(class_info_path, "r") as f:
                class_info = json.load(f)
                
            if "required_files" in class_info:
                structure += "│       └── Required Files:\n"
                for file_type in class_info["required_files"]:
                    structure += f"│           └── {file_type}.csv (needed)\n"
        except:
            pass
    
    structure += "├── reports/\n"
    structure += f"│   └── {date}/\n"
    structure += "│       ├── progress_reports/\n"
    structure += "│       │   ├── student_reports/\n"
    structure += "│       │   └── class_summaries/\n"
    structure += "│       ├── executive_reports/\n"
    structure += "│       │   ├── student_reports/\n"
    structure += "│       │   └── class_summaries/\n"
    structure += "│       ├── flexible_reports/\n"
    structure += "│       └── metrics/\n"
    
    return structure

# Dashboard API endpoints
@app.get("/api/v1/projects")
def get_projects():
    """Get a list of all projects (dates) with additional metadata"""
    try:
        # Get all available dates
        dates = get_available_dates()
        
        # For each date, get basic project info
        projects = []
        for date in dates:
            try:
                # Check if class_info.json exists
                class_info_path = os.path.join("assets", date, "class_info.json")
                project_info = {
                    "date": date,
                    "created_at": datetime.strptime(date, "%y-%m-%d").isoformat()
                }
                
                if os.path.exists(class_info_path):
                    with open(class_info_path, "r") as f:
                        class_info = json.load(f)
                        project_info["class_name"] = class_info.get("class_name", "Unknown Class")
                        project_info["current_module"] = class_info.get("current_module", 0)
                
                # Count number of students
                students_dir = os.path.join("assets", date, "students")
                if os.path.exists(students_dir):
                    project_info["student_count"] = len(os.listdir(students_dir))
                
                projects.append(project_info)
            except Exception as e:
                # If there's an error with a specific project, just add the date
                projects.append(date)
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving projects: {str(e)}")

@app.get("/api/v1/reports")
def get_all_reports():
    """Get a list of all generated reports across all dates"""
    try:
        # Get all available dates
        dates = get_available_dates()
        
        # For each date, get available reports
        all_reports = []
        for date in dates:
            try:
                reports = get_available_reports(date)
                
                # Add date and created_at to each report
                for report in reports:
                    report["date"] = date
                    report["created_at"] = datetime.strptime(date, "%y-%m-%d").isoformat()
                
                all_reports.extend(reports)
            except Exception as e:
                # If there's an error with a specific date, skip it
                continue
        
        return all_reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving reports: {str(e)}")

@app.get("/api/v1/health")
def health_check():
    """API health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/storage")
def storage_status():
    """Check storage status and available space"""
    try:
        # Check if assets directory exists
        if not os.path.exists("assets"):
            return {"status": "warning", "message": "Assets directory not found"}
        
        # Get storage usage information
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("assets"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        
        # Get disk usage for the current directory
        import shutil
        total, used, free = shutil.disk_usage(".")
        
        return {
            "status": "ok",
            "assets_size_bytes": total_size,
            "assets_size_mb": round(total_size / (1024 * 1024), 2),
            "disk_total_gb": round(total / (1024**3), 2),
            "disk_used_gb": round(used / (1024**3), 2),
            "disk_free_gb": round(free / (1024**3), 2),
            "disk_usage_percent": round((used / total) * 100, 2)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run the application with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for Railway)
    port = int(get_env_var("PORT", "8000"))
    
    # Determine if we should enable auto-reload
    reload_enabled = ENVIRONMENT != "production"
    
    print(f"Starting Cyber8 API server in {ENVIRONMENT} mode")
    print(f"Debug mode: {DEBUG}")
    print(f"Assets directory: {ASSETS_DIR}")
    print(f"Reports directory: {REPORTS_DIR}")
    print(f"Persistence enabled: {ENABLE_PERSISTENCE}")
    print(f"Listening on port: {port}")
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=reload_enabled)

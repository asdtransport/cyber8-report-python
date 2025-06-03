"""
Flexible assessment report generator.

This module provides functionality for generating flexible assessment grade reports.
"""
import sys
import os
import json
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Import utilities from compita package
from compita.utils.helpers import ensure_dir_exists
from compita.utils.logger import setup_logger

# Set up logger
logger = setup_logger('flexible_assessment')

def load_json_data(date_folder, file_name):
    """
    Load JSON data from a file.
    
    Args:
        date_folder (str): Date folder in YY-MM-DD format
        file_name (str): Name of the JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    # Try the legacy path first (which is now our primary path)
    file_path = f"assets/processed/{date_folder}/{file_name}"
    
    # If not found, try with the original CSV filename pattern
    if not os.path.exists(file_path):
        if file_name == 'classgradebook.json':
            possible_names = [
                f"assets/processed/{date_folder}/classgradebook-{date_folder.replace('-', '-')}-5pm.json",
                f"assets/processed/{date_folder}/classgradebook-{date_folder.split('-')[2]}-{date_folder.split('-')[1]}-5pm.json"
            ]
            for name in possible_names:
                if os.path.exists(name):
                    file_path = name
                    break
        elif file_name == 'studyhistory.json':
            possible_names = [
                f"assets/processed/{date_folder}/classstudyhistory-{date_folder.replace('-', '-')}-4pm.json",
                f"assets/processed/{date_folder}/classstudyhistory-{date_folder.split('-')[2]}-{date_folder.split('-')[1]}-4pm.json"
            ]
            for name in possible_names:
                if os.path.exists(name):
                    file_path = name
                    break
    
    # If still not found, try the new path
    if not os.path.exists(file_path):
        file_path = f"reports/{date_folder}/json/{file_name}"
    
    # If still not found, try searching for any matching JSON file in the directory
    if not os.path.exists(file_path):
        directory = f"assets/processed/{date_folder}"
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if file_name == 'classgradebook.json' and filename.startswith('classgradebook') and filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    break
                elif file_name == 'studyhistory.json' and filename.startswith('classstudyhistory') and filename.endswith('.json'):
                    file_path = os.path.join(directory, filename)
                    break
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {file_path}")
        return None

def process_assessment_data(gradebook_data, assessment_types, modules=None):
    """
    Process assessment grade data from the gradebook.
    
    Args:
        gradebook_data (dict): Gradebook data
        assessment_types (list): List of assessment types to include
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        dict: Processed assessment data
    """
    assessment_data = {}
    
    # Debug: Log the structure of the gradebook data
    logger.info(f"Assessment types: {assessment_types}")
    logger.info(f"Gradebook data keys: {list(gradebook_data.keys()) if isinstance(gradebook_data, dict) else 'Not a dict'}")
    
    # Check if the data is in the new format (list of students)
    if 'students' in gradebook_data:
        students = gradebook_data['students']
        logger.info(f"Found {len(students)} students in the gradebook data")
    else:
        # Assume the data is already a dictionary of student data
        students = [{'name': name, 'assessments': data} for name, data in gradebook_data.items()]
        logger.info(f"Converted {len(students)} students from dictionary format")
    
    # Get a sample student to understand the structure
    if students:
        sample_student = students[0]
        logger.info(f"Sample student keys: {list(sample_student.keys())}")
        if 'assessments' in sample_student:
            if isinstance(sample_student['assessments'], list):
                logger.info(f"Sample student has {len(sample_student['assessments'])} assessments as a list")
                if sample_student['assessments']:
                    logger.info(f"First assessment: {sample_student['assessments'][0]}")
            else:
                logger.info(f"Sample student assessments is not a list: {type(sample_student['assessments'])}")
    
    # Process each student's data
    for student in students:
        student_name = student['name']
        assessment_data[student_name] = {
            'assessments': {},
            'average_grade': 0,
            'total_assessments': 0,
            'completed_assessments': 0
        }
        
        # Initialize assessment types
        for assessment_type in assessment_types:
            assessment_data[student_name]['assessments'][assessment_type] = {}
        
        # Extract assessment grades
        total_grade = 0
        completed_count = 0
        quiz_count = 0
        lab_count = 0
        exam_count = 0
        
        # Process assessments
        if 'assessments' in student and isinstance(student['assessments'], list):
            # Process assessments array
            for assessment in student['assessments']:
                name = assessment.get('name', '')
                completion = assessment.get('completion', 0)
                
                # Skip if not an assessment
                if not name.startswith('Assessment'):
                    continue
                
                # Extract module number if possible
                module_num = None
                parts = name.split('.')
                if len(parts) > 1 and parts[0].startswith('Assessment - '):
                    try:
                        module_str = parts[0].replace('Assessment - ', '')
                        module_num = int(module_str)
                    except ValueError:
                        # Handle cases like 'Assessment - B.2.6' where the module isn't a number
                        if module_str.startswith('B.'):
                            module_str = module_str.replace('B.', '')
                            try:
                                module_num = int(module_str)
                            except ValueError:
                                pass
                
                # Skip if modules are specified and this assessment isn't in the requested modules
                if modules and (module_num is None or module_num not in modules):
                    continue
                    
                # Categorize assessment based on name
                if 'Module Quiz' in name:
                    assessment_type = 'Quiz'
                    quiz_count += 1
                    assessment_data[student_name]['assessments']['Quiz'][name] = completion
                elif 'Checkpoint Review' in name:
                    assessment_type = 'Exam'
                    exam_count += 1
                    assessment_data[student_name]['assessments']['Exam'][name] = completion
                elif 'Interactive' in name:
                    assessment_type = 'Quiz'
                    quiz_count += 1
                    assessment_data[student_name]['assessments']['Quiz'][name] = completion
                elif 'Lesson Review' in name:
                    assessment_type = 'Quiz'
                    quiz_count += 1
                    assessment_data[student_name]['assessments']['Quiz'][name] = completion
                else:
                    # Default to Quiz for other assessments
                    assessment_type = 'Quiz'
                    quiz_count += 1
                    assessment_data[student_name]['assessments']['Quiz'][name] = completion
                
                if completion > 0:  # Assessment was completed
                    completed_count += 1
                    total_grade += completion
        
        # Process labs if available
        if 'labs' in student and isinstance(student['labs'], list):
            logger.info(f"Processing {len(student['labs'])} labs for {student_name}")
            for lab in student['labs']:
                name = lab.get('name', '')
                completion = lab.get('completion', 0)
                
                # Extract module number if possible
                module_num = None
                parts = name.split('.')
                if len(parts) > 1 and parts[0].startswith('Lab - '):
                    try:
                        module_str = parts[0].replace('Lab - ', '')
                        module_num = int(module_str)
                    except ValueError:
                        # Handle cases like 'Lab - B.2.6' where the module isn't a number
                        if module_str.startswith('B.'):
                            module_str = module_str.replace('B.', '')
                            try:
                                module_num = int(module_str)
                            except ValueError:
                                pass
                
                # Skip if modules are specified and this lab isn't in the requested modules
                if modules and (module_num is None or module_num not in modules):
                    continue
                
                lab_count += 1
                assessment_data[student_name]['assessments']['Lab'][name] = completion
                
                if completion > 0:  # Lab was completed
                    completed_count += 1
                    total_grade += completion
        
        # Calculate average grade
        total_assessments = quiz_count + lab_count + exam_count
        assessment_data[student_name]['total_assessments'] = total_assessments
        assessment_data[student_name]['completed_assessments'] = completed_count
        
        if completed_count > 0:
            assessment_data[student_name]['average_grade'] = total_grade / completed_count
    
    # Log summary of processed data
    logger.info(f"Processed assessment data for {len(assessment_data)} students")
    if assessment_data:
        first_student = next(iter(assessment_data.values()))
        logger.info(f"First student assessment counts: Quiz={len(first_student['assessments']['Quiz'])}, Lab={len(first_student['assessments']['Lab'])}, Exam={len(first_student['assessments']['Exam'])}")
    
    return assessment_data

def generate_report(date_folder, assessment_types, output_prefix, modules=None):
    """
    Generate a flexible assessment grade report.
    
    Args:
        date_folder (str): Date folder in YY-MM-DD format
        assessment_types (list): List of assessment types to include
        output_prefix (str): Prefix for the output files
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Load gradebook data
    gradebook_data = load_json_data(date_folder, 'classgradebook.json')
    if not gradebook_data:
        return False
    
    # Process assessment data
    assessment_data = process_assessment_data(gradebook_data, assessment_types, modules)
    
    # Create output directory
    base_output_dir = f"reports/{date_folder}/flexible_reports"
    output_dir = f"{base_output_dir}/assessment_reports"
    ensure_dir_exists(output_dir)
    
    # Save results to JSON
    output_file = f"{output_dir}/{output_prefix}_assessment_grades.json"
    with open(output_file, 'w') as f:
        json.dump({
            'assessment_data': assessment_data,
            'metadata': {
                'date': date_folder,
                'assessment_types': assessment_types,
                'modules': modules
            }
        }, f, indent=2)
    
    logger.info(f"Assessment grade report saved to {output_file}")
    
    # Create CSV report
    csv_file = f"{output_dir}/{output_prefix}.csv"
    
    # Create DataFrame for CSV report
    data = []
    
    # Get assessment types for column headers
    assessment_types_str = '-'.join(assessment_type.split(' ')[0] for assessment_type in assessment_types)
    
    for student_name, student_data in assessment_data.items():
        row = {
            'Student': student_name,
            'Average Grade': student_data['average_grade'] * 100,  # Convert to percentage
            'Completed Assessments': student_data['completed_assessments'],
            'Total Assessments': student_data['total_assessments'],
            'Completion %': (student_data['completed_assessments'] / student_data['total_assessments'] * 100) if student_data['total_assessments'] > 0 else 0
        }
        
        # Add assessment type averages
        for assessment_type in assessment_types:
            assessments = student_data['assessments'][assessment_type]
            if assessments:
                grades = [grade for grade in assessments.values() if grade > 0]
                avg = sum(grades) / len(grades) * 100 if grades else 0
                row[f'{assessment_type} Average'] = avg
                row[f'{assessment_type} Count'] = len(grades)
            else:
                row[f'{assessment_type} Average'] = 0
                row[f'{assessment_type} Count'] = 0
        
        data.append(row)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    logger.info(f"CSV report saved to {csv_file}")
    
    # Create Excel report
    excel_file = f"{output_dir}/{output_prefix}.xlsx"
    
    # Create Excel writer
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Write summary sheet
        df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Create assessment-type-specific sheets
        for assessment_type in assessment_types:
            type_data = []
            
            for student_name, student_data in assessment_data.items():
                assessments = student_data['assessments'][assessment_type]
                
                # Create a row for each assessment
                for assessment_name, grade in assessments.items():
                    type_data.append({
                        'Student': student_name,
                        'Assessment': assessment_name,
                        'Grade': grade * 100  # Convert to percentage
                    })
            
            if type_data:
                type_df = pd.DataFrame(type_data)
                type_df.to_excel(writer, sheet_name=assessment_type[:30], index=False)  # Limit sheet name length
        
        # Add a dedicated sheet for Module Quizzes
        module_quiz_data = []
        for student_name, student_data in assessment_data.items():
            quiz_assessments = student_data['assessments']['Quiz']
            
            # Filter for Module Quizzes
            for assessment_name, grade in quiz_assessments.items():
                if 'Module Quiz' in assessment_name:
                    module_quiz_data.append({
                        'Student': student_name,
                        'Module Quiz': assessment_name,
                        'Grade': grade * 100  # Convert to percentage
                    })
        
        if module_quiz_data:
            module_quiz_df = pd.DataFrame(module_quiz_data)
            module_quiz_df.to_excel(writer, sheet_name='Module Quizzes', index=False)
        
        # Add configuration sheet
        config_data = {
            'Parameter': ['Date', 'Assessment Types'],
            'Value': [
                date_folder,
                ', '.join(assessment_types)
            ]
        }
        config_df = pd.DataFrame(config_data)
        config_df.to_excel(writer, sheet_name='Configuration', index=False)
    
    logger.info(f"Excel report saved to {excel_file}")
    
    return True

def generate_flexible_assessment_report(date, assessment_types=None, output_prefix=None, modules=None):
    """
    Generate a flexible assessment report.
    
    Args:
        date (str): Date in YY-MM-DD format
        assessment_types (list): List of assessment types to include
        output_prefix (str): Prefix for the output files
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Set default values
    if assessment_types is None:
        assessment_types = ['Quiz', 'Lab', 'Exam']
    
    if output_prefix is None:
        output_prefix = "flexible"
    
    # Generate the report
    return generate_report(date, assessment_types, output_prefix, modules)

def main():
    """
    Main function to parse command line arguments and execute the report generator.
    """
    parser = argparse.ArgumentParser(description='Generate a flexible assessment grade report.')
    parser.add_argument('--date', required=True, help='Date folder to process (format: YY-MM-DD)')
    parser.add_argument('--assessment-types', nargs='+', default=['Quiz', 'Lab', 'Exam'], 
                        help='List of assessment types to include')
    parser.add_argument('--output-prefix', default='flexible', 
                        help='Prefix for the output files')
    parser.add_argument('--modules', type=int, nargs='+',
                        help='List of module numbers to include (e.g., 1 2 3)')
    
    args = parser.parse_args()
    
    # Generate the report
    success = generate_flexible_assessment_report(
        args.date, 
        args.assessment_types, 
        args.output_prefix,
        args.modules
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

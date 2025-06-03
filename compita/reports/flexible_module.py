"""
Flexible module report generator.

This module provides functionality for generating flexible module completion reports.
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
logger = setup_logger('flexible_module')

def load_json_data(date_folder, file_name, assets_dir=None):
    """
    Load JSON data from a file.
    
    Args:
        date_folder (str): Date folder in YY-MM-DD format
        file_name (str): Name of the JSON file
        assets_dir (str): Custom assets directory path
        
    Returns:
        dict: Loaded JSON data
    """
    # Try the legacy path first (which is now our primary path)
    if assets_dir:
        file_path = f"{assets_dir}/processed/{date_folder}/{file_name}"
    else:
        file_path = f"assets/processed/{date_folder}/{file_name}"
    
    # If not found, try with the original CSV filename pattern
    if not os.path.exists(file_path):
        if file_name == 'classgradebook.json':
            possible_names = [
                f"{file_path.replace('-', '-')}-5pm.json",
                f"{file_path.replace('-', '-')}.json",
                f"{file_path.split('-')[2]}-{file_path.split('-')[1]}-{file_path.split('-')[0]}pm.json"
            ]
            for name in possible_names:
                if os.path.exists(name):
                    file_path = name
                    break
    
    # If still not found, try the new path
    if not os.path.exists(file_path):
        if assets_dir:
            file_path = f"{assets_dir}/reports/{date_folder}/json/{file_name}"
        else:
            file_path = f"reports/{date_folder}/json/{file_name}"
    
    # If still not found, try searching for any classgradebook JSON file in the directory
    if not os.path.exists(file_path) and file_name == 'classgradebook.json':
        if assets_dir:
            directory = f"{assets_dir}/processed/{date_folder}"
        else:
            directory = f"assets/processed/{date_folder}"
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.startswith('classgradebook') and filename.endswith('.json'):
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

def process_module_data(gradebook_data, all_modules, exclude_modules, count_partial=False):
    """
    Process module completion data from the gradebook.
    
    Args:
        gradebook_data (dict): Gradebook data
        all_modules (list): List of module numbers to include
        exclude_modules (list): List of module numbers to exclude
        count_partial (bool): Count partial completions as fully completed
        
    Returns:
        dict: Processed module data
    """
    module_data = {}
    
    # Check if the data is in the new format (list of students)
    if 'students' in gradebook_data:
        students = gradebook_data['students']
    else:
        # Assume the data is already a dictionary of student data
        students = [{'name': name, 'assessments': data} for name, data in gradebook_data.items()]
    
    # Process each student's data
    for student in students:
        student_name = student['name']
        module_data[student_name] = {
            'modules': {},
            'total_labs': 0,
            'completed_labs': 0,
            'completion_percentage': 0
        }
        
        # Count labs for each module
        for module_num in all_modules:
            # Skip excluded modules
            if module_num in exclude_modules:
                continue
                
            module_key = f"Module {module_num}"
            module_data[student_name]['modules'][module_key] = {
                'total_labs': 0,
                'completed_labs': 0,
                'completion_percentage': 0
            }
            
            # Check for lab completions for this module
            if 'labs' in student and isinstance(student['labs'], list):
                # Count labs for this module
                module_labs = []
                
                for lab in student['labs']:
                    lab_name = lab.get('name', '')
                    if f"Lab - {module_num}." in lab_name:
                        completion = lab.get('completion', 0)
                        is_completed = completion >= 0.8 or (count_partial and completion > 0)
                        
                        module_labs.append({
                            'name': lab_name,
                            'completion': completion,
                            'is_completed': is_completed
                        })
                
                # Update module data
                module_data[student_name]['modules'][module_key]['total_labs'] = len(module_labs)
                module_data[student_name]['modules'][module_key]['completed_labs'] = sum(1 for lab in module_labs if lab['is_completed'])
                
                # Calculate completion percentage for this module
                if len(module_labs) > 0:
                    module_data[student_name]['modules'][module_key]['completion_percentage'] = (
                        module_data[student_name]['modules'][module_key]['completed_labs'] / len(module_labs) * 100
                    )
                
                # Add to total counts
                module_data[student_name]['total_labs'] += len(module_labs)
                module_data[student_name]['completed_labs'] += module_data[student_name]['modules'][module_key]['completed_labs']
        
        # Calculate overall completion percentage
        if module_data[student_name]['total_labs'] > 0:
            module_data[student_name]['completion_percentage'] = (
                module_data[student_name]['completed_labs'] / module_data[student_name]['total_labs'] * 100
            )
    
    return module_data

def generate_report(date_folder, all_modules, subset_modules, exclude_modules, output_prefix, count_partial=False, output_dir=None):
    """
    Generate a flexible module completion report.
    
    Args:
        date_folder (str): Date folder in YY-MM-DD format
        all_modules (list): List of module numbers to include in the overall analysis
        subset_modules (list): List of module numbers to include in the subset analysis
        exclude_modules (list): List of module numbers to exclude from the overall analysis
        output_prefix (str): Prefix for the output files
        count_partial (bool): Count partial completions as fully completed
        output_dir (str): Custom output directory path
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Load gradebook data
    gradebook_data = load_json_data(date_folder, 'classgradebook.json')
    if not gradebook_data:
        return False
    
    # Process module data for all modules
    all_module_data = process_module_data(gradebook_data, all_modules, exclude_modules, count_partial)
    
    # Process module data for subset modules
    subset_module_data = None
    if subset_modules:
        subset_module_data = process_module_data(gradebook_data, subset_modules, [], count_partial)
    
    # Create output directory
    if output_dir:
        output_dir = f"{output_dir}/flexible_reports"
    else:
        output_dir = f"reports/{date_folder}/flexible_reports"
    ensure_dir_exists(output_dir)
    
    # Save results to JSON
    output_file = f"{output_dir}/{output_prefix}_module_completion.json"
    with open(output_file, 'w') as f:
        json.dump({
            'all_modules': all_module_data,
            'subset_modules': subset_module_data,
            'metadata': {
                'date': date_folder,
                'all_modules': all_modules,
                'subset_modules': subset_modules,
                'exclude_modules': exclude_modules,
                'count_partial': count_partial
            }
        }, f, indent=2)
    
    logger.info(f"Module completion report saved to {output_file}")
    
    # Create CSV report
    csv_file = f"{output_dir}/{output_prefix}.csv"
    
    # Create DataFrame for CSV report
    data = []
    
    # Get module strings for column headers
    all_modules_str = '-'.join(str(m) for m in all_modules if m not in exclude_modules)
    subset_modules_str = '-'.join(str(m) for m in subset_modules) if subset_modules else ''
    
    for student_name, student_data in all_module_data.items():
        row = {
            'Student': student_name,
            f'Total Labs {all_modules_str}': student_data['total_labs'],
            f'Completed Labs {all_modules_str}': student_data['completed_labs'],
            f'Labs {all_modules_str} Remaining': student_data['total_labs'] - student_data['completed_labs'],
            f'Labs {all_modules_str} Completion %': student_data['completion_percentage']
        }
        
        # Add subset data if available
        if subset_module_data and student_name in subset_module_data:
            subset_data = subset_module_data[student_name]
            row[f'Total Labs {subset_modules_str}'] = subset_data['total_labs']
            row[f'Completed Labs {subset_modules_str}'] = subset_data['completed_labs']
            row[f'Labs {subset_modules_str} Remaining'] = subset_data['total_labs'] - subset_data['completed_labs']
            row[f'Labs {subset_modules_str} Completion %'] = subset_data['completion_percentage']
        
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
        
        # Create module-specific sheets
        for module_num in all_modules:
            if module_num in exclude_modules:
                continue
                
            module_key = f"Module {module_num}"
            module_data = []
            
            for student_name, student_data in all_module_data.items():
                module_data.append({
                    'Student': student_name,
                    f'{module_key} Total Labs': student_data['modules'][module_key]['total_labs'],
                    f'{module_key} Completed Labs': student_data['modules'][module_key]['completed_labs'],
                    f'{module_key} Labs Remaining': student_data['modules'][module_key]['total_labs'] - student_data['modules'][module_key]['completed_labs'],
                    f'{module_key} Labs Completion %': student_data['modules'][module_key]['completion_percentage']
                })
            
            module_df = pd.DataFrame(module_data)
            module_df.to_excel(writer, sheet_name=f'Module {module_num}', index=False)
        
        # Add configuration sheet
        config_data = {
            'Parameter': ['Date', 'All Modules', 'Subset Modules', 'Excluded Modules', 'Count Partial Completions'],
            'Value': [
                date_folder,
                ', '.join(str(m) for m in all_modules),
                ', '.join(str(m) for m in subset_modules) if subset_modules else 'None',
                ', '.join(str(m) for m in exclude_modules) if exclude_modules else 'None',
                'Yes' if count_partial else 'No'
            ]
        }
        config_df = pd.DataFrame(config_data)
        config_df.to_excel(writer, sheet_name='Configuration', index=False)
    
    logger.info(f"Excel report saved to {excel_file}")
    
    return True

def generate_flexible_module_report(date, all_modules=None, subset_modules=None, exclude_modules=None, 
                                   output_prefix=None, count_partial=False, assets_dir=None, output_dir=None):
    """
    Generate a flexible module report.
    
    Args:
        date (str): Date in YY-MM-DD format
        all_modules (list): List of module numbers to include in the overall analysis
        subset_modules (list): List of module numbers to include in the subset analysis
        exclude_modules (list): List of module numbers to exclude from the overall analysis
        output_prefix (str): Prefix for the output files
        count_partial (bool): Count partial completions as fully completed
        assets_dir (str): Custom assets directory path
        output_dir (str): Custom output directory path
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Set default values
    if all_modules is None:
        all_modules = [str(i) for i in range(1, 7)]  # Modules 1-6
    
    if subset_modules is None:
        subset_modules = []
    
    if exclude_modules is None:
        exclude_modules = []
    
    if output_prefix is None:
        output_prefix = "flexible"
    
    # Generate the report
    return generate_report(date, all_modules, subset_modules, exclude_modules, output_prefix, count_partial, output_dir)

def main():
    """
    Main function to parse command line arguments and execute the report generator.
    """
    parser = argparse.ArgumentParser(description='Generate a flexible module completion report.')
    parser.add_argument('--date', required=True, help='Date folder to process (format: YY-MM-DD)')
    parser.add_argument('--all-modules', nargs='+', default=[str(i) for i in range(1, 7)], 
                        help='List of module numbers to include in the overall analysis')
    parser.add_argument('--subset-modules', nargs='+', default=[], 
                        help='List of module numbers to include in the subset analysis')
    parser.add_argument('--exclude-modules', nargs='+', default=[], 
                        help='List of module numbers to exclude from the overall analysis')
    parser.add_argument('--output-prefix', default='flexible', 
                        help='Prefix for the output files')
    parser.add_argument('--count-partial', action='store_true', 
                        help='Count partial completions as fully completed')
    parser.add_argument('--assets-dir', default=None, 
                        help='Custom assets directory path')
    parser.add_argument('--output-dir', default=None, 
                        help='Custom output directory path')
    
    args = parser.parse_args()
    
    # Generate the report
    success = generate_flexible_module_report(
        args.date, 
        args.all_modules, 
        args.subset_modules, 
        args.exclude_modules, 
        args.output_prefix, 
        args.count_partial,
        args.assets_dir,
        args.output_dir
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

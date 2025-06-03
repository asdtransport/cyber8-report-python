"""
Flexible grades report generator.

This module provides functionality for generating flexible grade reports.
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
logger = setup_logger('flexible_grades')

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
    
    # If still not found, try the new path
    if not os.path.exists(file_path):
        file_path = f"reports/{date_folder}/json/{file_name}"
    
    # If still not found, try searching for any matching JSON file in the directory
    if not os.path.exists(file_path) and file_name == 'classgradebook.json':
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

def process_grades_data(gradebook_data, grade_categories, grade_weights=None, modules=None):
    """
    Process grade data from the gradebook.
    
    Args:
        gradebook_data (dict): Gradebook data
        grade_categories (list): List of grade categories to include
        grade_weights (dict): Weights for each grade category
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        dict: Processed grade data
    """
    if grade_weights is None:
        # Default weights if none provided
        grade_weights = {category: 1.0 for category in grade_categories}
    
    # Normalize weights
    total_weight = sum(grade_weights.values())
    normalized_weights = {k: v / total_weight for k, v in grade_weights.items()}
    
    grades_data = {}
    
    # Check if the data is in the new format (list of students)
    if 'students' in gradebook_data:
        students = gradebook_data['students']
    else:
        # Assume the data is already a dictionary of student data
        students = [{'name': name, 'assessments': data} for name, data in gradebook_data.items()]
    
    # Process each student's data
    for student in students:
        student_name = student['name']
        grades_data[student_name] = {
            'categories': {},
            'weighted_average': 0,
            'overall_average': 0,
            'modules': {}
        }
        
        # Initialize categories
        for category in grade_categories:
            grades_data[student_name]['categories'][category] = {
                'average': 0,
                'count': 0,
                'grades': []
            }
            
            # Initialize modules data if modules are specified
            if modules:
                grades_data[student_name]['modules'] = {}
                for module in modules:
                    grades_data[student_name]['modules'][str(module)] = {
                        'categories': {}
                    }
                    for category in grade_categories:
                        grades_data[student_name]['modules'][str(module)]['categories'][category] = {
                            'average': 0,
                            'count': 0,
                            'grades': []
                        }
        
        # Process assessments
        if 'assessments' in student and isinstance(student['assessments'], list):
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
                category = None
                if 'Module Quiz' in name or 'Interactive' in name or 'Lesson Review' in name:
                    category = 'Quiz'
                elif 'Checkpoint Review' in name:
                    category = 'Exam'
                
                # Add to appropriate category if it matches one of our categories
                if category in grade_categories and completion > 0:
                    # Add to overall category grades
                    grades_data[student_name]['categories'][category]['grades'].append(completion)
                    
                    # Add to module-specific category if applicable
                    if modules and module_num in modules:
                        grades_data[student_name]['modules'][str(module_num)]['categories'][category]['grades'].append(completion)
        
        # Process labs if available and if 'Lab' is in grade_categories
        if 'Lab' in grade_categories and 'labs' in student and isinstance(student['labs'], list):
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
                
                if completion > 0:
                    # Add to overall Lab category
                    grades_data[student_name]['categories']['Lab']['grades'].append(completion)
                    
                    # Add to module-specific category if applicable
                    if modules and module_num in modules:
                        grades_data[student_name]['modules'][str(module_num)]['categories']['Lab']['grades'].append(completion)
        
        # Calculate category averages for overall categories
        category_averages = {}
        for category in grade_categories:
            grades = grades_data[student_name]['categories'][category]['grades']
            if grades:
                category_avg = sum(grades) / len(grades)
                count = len(grades)
            else:
                category_avg = 0
                count = 0
                
            category_averages[category] = category_avg
            grades_data[student_name]['categories'][category]['average'] = category_avg
            grades_data[student_name]['categories'][category]['count'] = count
            # Remove the grades array to keep the JSON cleaner
            grades_data[student_name]['categories'][category].pop('grades', None)
        
        # Calculate module-specific category averages if modules are specified
        if modules:
            for module in modules:
                module_str = str(module)
                module_category_averages = {}
                
                for category in grade_categories:
                    grades = grades_data[student_name]['modules'][module_str]['categories'][category]['grades']
                    if grades:
                        category_avg = sum(grades) / len(grades)
                        count = len(grades)
                    else:
                        category_avg = 0
                        count = 0
                    
                    module_category_averages[category] = category_avg
                    grades_data[student_name]['modules'][module_str]['categories'][category]['average'] = category_avg
                    grades_data[student_name]['modules'][module_str]['categories'][category]['count'] = count
                    # Remove the grades array to keep the JSON cleaner
                    grades_data[student_name]['modules'][module_str]['categories'][category].pop('grades', None)
                
                # Calculate module-specific overall average
                valid_module_categories = [avg for avg in module_category_averages.values() if avg > 0]
                if valid_module_categories:
                    grades_data[student_name]['modules'][module_str]['overall_average'] = sum(valid_module_categories) / len(valid_module_categories)
                else:
                    grades_data[student_name]['modules'][module_str]['overall_average'] = 0
                
                # Calculate module-specific weighted average
                module_weighted_sum = 0
                module_weight_used = 0
                for category, avg in module_category_averages.items():
                    if avg > 0:  # Only include categories with grades
                        weight = normalized_weights.get(category, 0)
                        module_weighted_sum += avg * weight
                        module_weight_used += weight
                
                if module_weight_used > 0:
                    grades_data[student_name]['modules'][module_str]['weighted_average'] = module_weighted_sum / module_weight_used
                else:
                    grades_data[student_name]['modules'][module_str]['weighted_average'] = 0
        
        # Calculate overall average (unweighted)
        valid_categories = [avg for avg in category_averages.values() if avg > 0]
        if valid_categories:
            grades_data[student_name]['overall_average'] = sum(valid_categories) / len(valid_categories)
        
        # Calculate weighted average
        weighted_sum = 0
        weight_used = 0
        for category, avg in category_averages.items():
            if avg > 0:  # Only include categories with grades
                weight = normalized_weights.get(category, 0)
                weighted_sum += avg * weight
                weight_used += weight
        
        if weight_used > 0:
            grades_data[student_name]['weighted_average'] = weighted_sum / weight_used
        
        # Remove modules data if it's empty
        if modules and 'modules' in grades_data[student_name]:
            try:
                if all(len(m['categories'][c].get('grades', [])) == 0 for m in grades_data[student_name]['modules'].values() for c in grade_categories):
                    grades_data[student_name].pop('modules', None)
            except KeyError:
                # If any expected keys are missing, just keep the modules data as is
                pass
    
    return grades_data

def generate_report(date_folder, grade_categories, grade_weights, output_prefix, modules=None):
    """
    Generate a flexible grades report.
    
    Args:
        date_folder (str): Date folder in YY-MM-DD format
        grade_categories (list): List of grade categories to include
        grade_weights (dict): Weights for each grade category
        output_prefix (str): Prefix for the output files
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Load gradebook data
    gradebook_data = load_json_data(date_folder, 'classgradebook.json')
    if not gradebook_data:
        return False
    
    # Process grades data
    grades_data = process_grades_data(gradebook_data, grade_categories, grade_weights, modules)
    
    # Create output directory
    base_output_dir = f"reports/{date_folder}/flexible_reports"
    output_dir = f"{base_output_dir}/grades_reports"
    ensure_dir_exists(output_dir)
    
    # Create module-specific directory suffix if modules are specified
    module_suffix = ""
    if modules:
        module_suffix = f"_modules_{'_'.join(str(m) for m in modules)}"
        output_dir = f"{output_dir}/modules_{'_'.join(str(m) for m in modules)}"
        ensure_dir_exists(output_dir)
    
    # Save results to JSON
    output_file = f"{output_dir}/{output_prefix}{module_suffix}_grades.json"
    with open(output_file, 'w') as f:
        json.dump({
            'grades_data': grades_data,
            'metadata': {
                'date': date_folder,
                'grade_categories': grade_categories,
                'grade_weights': grade_weights,
                'modules': modules
            }
        }, f, indent=2)
    
    logger.info(f"Grades report saved to {output_file}")
    
    # Create CSV report
    csv_file = f"{output_dir}/{output_prefix}{module_suffix}.csv"
    
    # Create DataFrame for CSV report
    data = []
    
    # Get grade categories for column headers
    categories_str = '-'.join(cat.split(' ')[0] for cat in grade_categories)
    
    for student_name, student_data in grades_data.items():
        row = {
            'Student': student_name,
            'Overall Average': student_data['overall_average'] * 100,  # Convert to percentage
            'Weighted Average': student_data['weighted_average'] * 100  # Convert to percentage
        }
        
        # Add category averages
        for category in grade_categories:
            if category in student_data['categories']:
                cat_data = student_data['categories'][category]
                row[f'{category} Average'] = cat_data['average'] * 100  # Convert to percentage
                row[f'{category} Count'] = cat_data['count']
            else:
                row[f'{category} Average'] = 0
                row[f'{category} Count'] = 0
        
        data.append(row)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    logger.info(f"CSV report saved to {csv_file}")
    
    # Create Excel report
    excel_file = f"{output_dir}/{output_prefix}{module_suffix}.xlsx"
    
    # Create Excel writer
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Write summary sheet
        df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Create category-specific sheets
        for category in grade_categories:
            category_data = []
            
            for student_name, student_data in grades_data.items():
                if category in student_data['categories']:
                    cat_data = student_data['categories'][category]
                    category_data.append({
                        'Student': student_name,
                        'Average': cat_data['average'] * 100,  # Convert to percentage
                        'Count': cat_data['count']
                    })
            
            if category_data:
                category_df = pd.DataFrame(category_data)
                category_df.to_excel(writer, sheet_name=category[:30], index=False)  # Limit sheet name length
        
        # Create module-specific sheets if modules are specified
        if modules:
            # Create a summary sheet for all modules
            module_summary_data = []
            
            for student_name, student_data in grades_data.items():
                if 'modules' in student_data:
                    for module_num, module_data in student_data['modules'].items():
                        row = {
                            'Student': student_name,
                            'Module': module_num,
                            'Overall Average': module_data.get('overall_average', 0) * 100,  # Convert to percentage
                            'Weighted Average': module_data.get('weighted_average', 0) * 100  # Convert to percentage
                        }
                        
                        # Add category averages for this module
                        for category in grade_categories:
                            if category in module_data['categories']:
                                cat_data = module_data['categories'][category]
                                row[f'{category} Average'] = cat_data['average'] * 100  # Convert to percentage
                                row[f'{category} Count'] = cat_data['count']
                            else:
                                row[f'{category} Average'] = 0
                                row[f'{category} Count'] = 0
                        
                        module_summary_data.append(row)
            
            if module_summary_data:
                module_summary_df = pd.DataFrame(module_summary_data)
                module_summary_df.to_excel(writer, sheet_name='Module Summary', index=False)
            
            # Create individual sheets for each module
            for module in modules:
                module_str = str(module)
                module_data = []
                
                for student_name, student_data in grades_data.items():
                    if 'modules' in student_data and module_str in student_data['modules']:
                        mod_data = student_data['modules'][module_str]
                        row = {
                            'Student': student_name,
                            'Overall Average': mod_data.get('overall_average', 0) * 100,  # Convert to percentage
                            'Weighted Average': mod_data.get('weighted_average', 0) * 100  # Convert to percentage
                        }
                        
                        # Add category averages for this module
                        for category in grade_categories:
                            if category in mod_data['categories']:
                                cat_data = mod_data['categories'][category]
                                row[f'{category} Average'] = cat_data['average'] * 100  # Convert to percentage
                                row[f'{category} Count'] = cat_data['count']
                            else:
                                row[f'{category} Average'] = 0
                                row[f'{category} Count'] = 0
                        
                        module_data.append(row)
                
                if module_data:
                    module_df = pd.DataFrame(module_data)
                    module_df.to_excel(writer, sheet_name=f'Module {module}', index=False)
        
        # Add configuration sheet
        config_params = ['Date', 'Grade Categories', 'Grade Weights']
        config_values = [
            date_folder,
            ', '.join(grade_categories),
            ', '.join([f"{k}: {v}" for k, v in grade_weights.items()])
        ]
        
        if modules:
            config_params.append('Modules')
            config_values.append(', '.join([str(m) for m in modules]))
        
        config_data = {
            'Parameter': config_params,
            'Value': config_values
        }
        config_df = pd.DataFrame(config_data)
        config_df.to_excel(writer, sheet_name='Configuration', index=False)
    
    logger.info(f"Excel report saved to {excel_file}")
    
    return True

def generate_flexible_grades_report(date, grade_categories=None, grade_weights=None, output_prefix=None, modules=None):
    """
    Generate a flexible grades report.
    
    Args:
        date (str): Date in YY-MM-DD format
        grade_categories (list): List of grade categories to include
        grade_weights (dict): Weights for each grade category
        output_prefix (str): Prefix for the output files
        modules (list): List of module numbers to include (e.g., [1, 2, 3])
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Set default values
    if grade_categories is None:
        grade_categories = ['Quiz', 'Lab', 'Exam']
    
    if grade_weights is None:
        grade_weights = {category: 1.0 for category in grade_categories}
    
    if output_prefix is None:
        output_prefix = "flexible"
    
    # Generate the report
    return generate_report(date, grade_categories, grade_weights, output_prefix, modules)

def main():
    """
    Main function to parse command line arguments and execute the report generator.
    """
    parser = argparse.ArgumentParser(description='Generate a flexible grades report.')
    parser.add_argument('--date', required=True, help='Date folder to process (format: YY-MM-DD)')
    parser.add_argument('--grade-categories', nargs='+', default=['Quiz', 'Lab', 'Exam'], 
                        help='List of grade categories to include')
    parser.add_argument('--output-prefix', default='flexible', 
                        help='Prefix for the output files')
    parser.add_argument('--quiz-weight', type=float, default=0.3, 
                        help='Weight for Quiz grades')
    parser.add_argument('--lab-weight', type=float, default=0.3, 
                        help='Weight for Lab grades')
    parser.add_argument('--exam-weight', type=float, default=0.4, 
                        help='Weight for Exam grades')
    parser.add_argument('--modules', type=int, nargs='+',
                        help='List of module numbers to include (e.g., 1 2 3)')
    
    args = parser.parse_args()
    
    # Build weights dictionary
    weights = {}
    if 'Quiz' in args.grade_categories:
        weights['Quiz'] = args.quiz_weight
    if 'Lab' in args.grade_categories:
        weights['Lab'] = args.lab_weight
    if 'Exam' in args.grade_categories:
        weights['Exam'] = args.exam_weight
    
    # Generate the report
    success = generate_flexible_grades_report(
        args.date, 
        args.grade_categories, 
        weights, 
        args.output_prefix,
        args.modules
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

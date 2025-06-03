# CompITA Report Generator Transformation Plan

## Executive Summary

This document outlines a comprehensive plan to transform the CompITA Report Generator from a specialized CSV-to-report tool into a flexible, LLM-powered framework capable of processing any CSV data into customized reports. The plan leverages existing components while introducing a modular architecture that supports both local execution and cloud-based SaaS deployment.

## Current System Analysis

### Overview

The CompITA Report Generator is a Python-based system that processes CSV data into structured reports through several key stages:

1. **CSV Parsing**: Converts raw CSV files to JSON format with standardized structure
2. **Metrics Collection**: Processes the JSON data to extract and calculate metrics
3. **Report Generation**: Creates markdown reports from the metrics
4. **PDF Conversion**: Transforms markdown reports into professionally formatted PDFs

### Key Components and Files

| Component | Key Files | Description |
|-----------|-----------|-------------|
| CLI Interface | `/compita-cli.py`, `/compita/cli/commands.py` | Command-line interface for running the report generation process |
| CSV Parser | `/compita/parsers/csv_parser.py` | Parses different types of CSV files into standardized JSON |
| Metrics Collector | `/compita/collectors/metrics_collector.py` | Aggregates data and calculates metrics |
| Report Generator | `/compita/reports/report_generator.py`, `/compita/reports/report_formatter.py` | Generates markdown reports from metrics |
| PDF Converter | `/compita/converters/markdown_to_pdf.py` | Converts markdown to PDF with professional formatting |

### Current Workflow

1. CSV files are placed in `assets/comptia/{date}` directory
2. CLI commands process these files through the pipeline:
   ```
   ./compita-cli.py generate-all --date YY-MM-DD
   ```
3. Reports are generated in `reports/{date}` directory
4. Final PDFs are created in `reports/{date}/executive_reports`

## Transformation Vision

Transform the CompITA Report Generator into a flexible framework that can:

1. Accept any CSV data structure
2. Use LLMs to dynamically analyze and parse CSV files
3. Generate customized metrics and reports
4. Support multiple output formats (markdown, HTML, PDF)
5. Run both locally and as a cloud-based SaaS
6. Maintain security for sensitive environments

## Development Plan

### Phase 1: Modularization and Abstraction (2-3 Months)

#### 1.1 Create Abstract Base Classes

**Files to Create/Modify:**
- `/compita/core/base_parser.py`
- `/compita/core/base_processor.py`
- `/compita/core/base_generator.py`
- `/compita/core/base_formatter.py`

**Example Implementation:**

```python
# /compita/core/base_parser.py
from abc import ABC, abstractmethod

class BaseCSVParser(ABC):
    """Base class for all CSV parsers."""
    
    @abstractmethod
    def parse(self, csv_file_path, output_dir):
        """
        Parse a CSV file and convert it to a standardized format.
        
        Args:
            csv_file_path (str): Path to the CSV file
            output_dir (str): Directory to save the output
            
        Returns:
            dict: Parsed data
        """
        pass
```

#### 1.2 Refactor Existing Components

**Files to Modify:**
- `/compita/parsers/csv_parser.py` → Implement `BaseCSVParser`
- `/compita/collectors/metrics_collector.py` → Implement `BaseProcessor`
- `/compita/reports/report_generator.py` → Implement `BaseGenerator`
- `/compita/converters/markdown_to_pdf.py` → Implement `BaseFormatter`

#### 1.3 Implement Plugin Architecture

**Files to Create:**
- `/compita/core/plugin_manager.py`

**Example Implementation:**

```python
# /compita/core/plugin_manager.py
class PluginManager:
    """Manages plugins for the report generation pipeline."""
    
    def __init__(self):
        self.parsers = {}
        self.processors = {}
        self.generators = {}
        self.formatters = {}
    
    def register_parser(self, name, parser_class):
        """Register a parser plugin."""
        self.parsers[name] = parser_class
    
    def get_parser(self, name):
        """Get a parser plugin by name."""
        return self.parsers.get(name)
    
    # Similar methods for processors, generators, and formatters
```

#### 1.4 Create Configuration System

**Files to Create:**
- `/compita/core/config_manager.py`
- `/compita/templates/config_schema.json`

### Phase 2: LLM Integration (3-4 Months)

#### 2.1 CSV Analysis Module

**Files to Create:**
- `/compita/llm/csv_analyzer.py`
- `/compita/llm/llm_service.py`

**Example Implementation:**

```python
# /compita/llm/csv_analyzer.py
import pandas as pd

class LLMCSVAnalyzer:
    """Uses LLM to analyze CSV structure and content."""
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    def analyze_csv(self, csv_file_path, sample_rows=10):
        """
        Analyze a CSV file using LLM.
        
        Args:
            csv_file_path (str): Path to the CSV file
            sample_rows (int): Number of rows to sample
            
        Returns:
            dict: CSV schema and analysis
        """
        # Read sample of CSV data
        sample_data = self._read_sample(csv_file_path, sample_rows)
        
        # Generate prompt for LLM
        prompt = self._generate_analysis_prompt(sample_data)
        
        # Get LLM response
        response = self.llm_service.generate(prompt)
        
        # Parse response into schema
        schema = self._parse_schema_from_response(response)
        
        return schema
    
    def _read_sample(self, csv_file_path, sample_rows):
        """Read a sample of rows from a CSV file."""
        df = pd.read_csv(csv_file_path, nrows=sample_rows)
        return df.to_string()
    
    def _generate_analysis_prompt(self, sample_data):
        """Generate a prompt for the LLM to analyze the CSV data."""
        return f"""
        Analyze the following CSV data sample and provide:
        1. A description of each column (name, data type, possible values)
        2. Potential metrics that could be calculated from this data
        3. Suggested report sections based on the data content
        
        CSV Sample:
        {sample_data}
        """
    
    def _parse_schema_from_response(self, response):
        """Parse the LLM response into a structured schema."""
        # Implementation depends on LLM response format
        # This would extract column definitions, metrics, and report sections
        return {
            "columns": [],
            "suggested_metrics": [],
            "suggested_report_sections": []
        }
```

#### 2.2 Dynamic Parser Generator

**Files to Create:**
- `/compita/llm/parser_generator.py`

#### 2.3 Metrics Suggestion Engine

**Files to Create:**
- `/compita/llm/metrics_suggester.py`

### Phase 3: Report Template System (2-3 Months)

#### 3.1 Template Engine

**Files to Create/Modify:**
- `/compita/templates/report_templates/`
- `/compita/core/template_engine.py`

#### 3.2 Visualization Components

**Files to Create:**
- `/compita/visualizations/`
- `/compita/visualizations/chart_generator.py`

### Phase 4: Cloud Infrastructure (4-5 Months)

#### 4.1 API Development

**Files to Create:**
- `/api/` (new directory)
- `/api/routes/`
- `/api/models/`
- `/api/controllers/`

#### 4.2 DevOps Pipeline

**Files to Create:**
- `/.github/workflows/` or `/gitlab-ci.yml`
- `/Dockerfile`
- `/docker-compose.yml`

#### 4.3 SaaS Platform

**Files to Create:**
- `/web/` (new directory for web interface)

### Phase 5: Security and Compliance (2-3 Months)

#### 5.1 Local Execution Mode

**Files to Create/Modify:**
- `/compita/core/execution_manager.py`

#### 5.2 Compliance Features

**Files to Create:**
- `/compita/security/anonymizer.py`
- `/compita/security/audit_logger.py`

## Prototype Development Method

To accelerate the transformation process and validate the new architecture, we'll develop a prototype that leverages the existing codebase while introducing the new modular components. This approach allows us to test the new architecture incrementally without disrupting the current functionality.

### Step 1: Create Core Abstract Classes

First, we'll implement the core abstract classes that will form the foundation of our new architecture:

```python
# /compita/core/base_parser.py
from abc import ABC, abstractmethod

class BaseCSVParser(ABC):
    @abstractmethod
    def parse(self, csv_file_path, output_dir):
        pass

# /compita/core/base_processor.py
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, parsed_data, output_dir):
        pass

# /compita/core/base_generator.py
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, metrics_data, output_dir):
        pass

# /compita/core/base_formatter.py
from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    @abstractmethod
    def format(self, report_data, output_dir):
        pass
```

### Step 2: Create Adapter Classes for Existing Components

Next, we'll create adapter classes that wrap the existing components to implement the new interfaces:

```python
# /compita/adapters/csv_parser_adapter.py
from compita.core.base_parser import BaseCSVParser
from compita.parsers.csv_parser import parse_csv_to_json, parse_resource_time_to_json, parse_study_history_to_json

class GradebookCSVParserAdapter(BaseCSVParser):
    def parse(self, csv_file_path, output_dir):
        return parse_csv_to_json(csv_file_path, output_dir)

class ResourceTimeCSVParserAdapter(BaseCSVParser):
    def parse(self, csv_file_path, output_dir):
        return parse_resource_time_to_json(csv_file_path, output_dir)

class StudyHistoryCSVParserAdapter(BaseCSVParser):
    def parse(self, csv_file_path, output_dir):
        return parse_study_history_to_json(csv_file_path, output_dir)
```

### Step 3: Implement Plugin Manager

Create a plugin manager to register and manage the different components:

```python
# /compita/core/plugin_manager.py
class PluginManager:
    """Manages plugins for the report generation pipeline."""
    
    def __init__(self):
        self.parsers = {}
        self.processors = {}
        self.generators = {}
        self.formatters = {}
    
    def register_parser(self, name, parser_class):
        """Register a parser plugin."""
        self.parsers[name] = parser_class
    
    def get_parser(self, name):
        """Get a parser plugin by name."""
        return self.parsers.get(name)
    
    # Similar methods for processors, generators, and formatters
```

### Step 4: Create a Simple LLM Service

Implement a basic LLM service for testing the integration:

```python
# /compita/llm/llm_service.py
import requests

class LLMService:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
    
    def generate(self, prompt):
        """
        Generate a response from the LLM.
        
        Args:
            prompt (str): The prompt to send to the LLM
            
        Returns:
            str: The LLM response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["text"]
        else:
            raise Exception(f"LLM API error: {response.status_code} - {response.text}")
```

### Step 5: Create a CSV Analyzer Using LLM

Implement a CSV analyzer that uses the LLM service:

```python
# /compita/llm/csv_analyzer.py
import pandas as pd
import json

class CSVAnalyzer:
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    def analyze_csv(self, csv_file_path, sample_rows=10):
        """
        Analyze a CSV file using LLM.
        
        Args:
            csv_file_path (str): Path to the CSV file
            sample_rows (int): Number of rows to sample
            
        Returns:
            dict: CSV schema and analysis
        """
        # Read sample of CSV data
        sample_data = self._read_sample(csv_file_path, sample_rows)
        
        # Generate prompt for LLM
        prompt = self._generate_analysis_prompt(sample_data)
        
        # Get LLM response
        response = self.llm_service.generate(prompt)
        
        # Parse response into schema
        schema = self._parse_schema_from_response(response)
        
        return schema
    
    def _read_sample(self, csv_file_path, sample_rows):
        """Read a sample of rows from a CSV file."""
        df = pd.read_csv(csv_file_path, nrows=sample_rows)
        return df.to_string()
    
    def _generate_analysis_prompt(self, sample_data):
        """Generate a prompt for the LLM to analyze the CSV data."""
        return f"""
        You are an expert data analyst. Analyze the following CSV data sample and provide:
        1. A description of each column (name, data type, possible values)
        2. Potential metrics that could be calculated from this data
        3. Suggested report sections based on the data content
        
        Format your response as JSON with the following structure:
        {{
            "columns": [
                {{
                    "name": "column_name",
                    "data_type": "string|number|date|boolean",
                    "description": "Description of the column",
                    "possible_values": ["value1", "value2"] // if applicable
                }}
            ],
            "suggested_metrics": [
                {{
                    "name": "metric_name",
                    "description": "Description of the metric",
                    "calculation": "How to calculate the metric"
                }}
            ],
            "suggested_report_sections": [
                {{
                    "title": "Section Title",
                    "content": "Description of what should be in this section",
                    "metrics": ["metric1", "metric2"]
                }}
            ]
        }}
        
        CSV Sample:
        {sample_data}
        """
    
    def _parse_schema_from_response(self, response):
        """Parse the LLM response into a structured schema."""
        try:
            # Extract JSON from the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            # Parse JSON
            schema = json.loads(json_str)
            return schema
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing LLM response: {e}")
            # Return a basic schema if parsing fails
            return {
                "columns": [],
                "suggested_metrics": [],
                "suggested_report_sections": []
            }
```

### Step 6: Create a Configuration-Based CLI

Develop a new CLI that uses the pipeline orchestrator and configuration:

```python
# /compita/cli/new_cli.py
#!/usr/bin/env python3
"""
Enhanced CompITA Report Generator CLI
"""
import argparse
import json
import os
import sys

from compita.core.plugin_manager import PluginManager
from compita.core.pipeline_orchestrator import PipelineOrchestrator
from compita.adapters.csv_parser_adapter import GradebookCSVParserAdapter, ResourceTimeCSVParserAdapter, StudyHistoryCSVParserAdapter
from compita.adapters.metrics_processor_adapter import MetricsProcessorAdapter
from compita.adapters.report_generator_adapter import MarkdownReportGeneratorAdapter
from compita.adapters.formatter_adapter import PDFFormatterAdapter

def register_default_plugins():
    """Register default plugins with the plugin manager."""
    plugin_manager = PluginManager()
    
    # Register parsers
    plugin_manager.register_parser("gradebook", GradebookCSVParserAdapter)
    plugin_manager.register_parser("resource_time", ResourceTimeCSVParserAdapter)
    plugin_manager.register_parser("study_history", StudyHistoryCSVParserAdapter)
    
    # Register processors
    plugin_manager.register_processor("metrics", MetricsProcessorAdapter)
    
    # Register generators
    plugin_manager.register_generator("markdown", MarkdownReportGeneratorAdapter)
    
    # Register formatters
    plugin_manager.register_formatter("pdf", PDFFormatterAdapter)
    
    return plugin_manager

def main():
    """Main function to parse command line arguments and execute the pipeline."""
    parser = argparse.ArgumentParser(description='Enhanced CompITA Report Generator')
    parser.add_argument('--config', help='Path to pipeline configuration file')
    parser.add_argument('--date', required=True, help='Date in YY-MM-DD format')
    parser.add_argument('--assets-dir', default='assets', help='Path to assets directory')
    parser.add_argument('--output-dir', default='reports', help='Path to output directory')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        # Use default configuration
        config = {
            "parser": {
                "name": "gradebook",
                "args": {
                    "csv_file_path": f"{args.assets_dir}/comptia/{args.date}/classgradebook.csv",
                    "output_dir": f"{args.assets_dir}/processed/{args.date}"
                }
            },
            "processor": {
                "name": "metrics",
                "args": {
                    "date_folder": args.date,
                    "output_dir": f"{args.output_dir}/{args.date}/metrics"
                }
            },
            "generator": {
                "name": "markdown",
                "args": {
                    "date": args.date,
                    "output_dir": f"{args.output_dir}/{args.date}/progress_reports"
                }
            },
            "formatter": {
                "name": "pdf",
                "args": {
                    "input_dir": f"{args.output_dir}/{args.date}/progress_reports",
                    "output_dir": f"{args.output_dir}/{args.date}/executive_reports"
                }
            }
        }
    
    # Register default plugins
    plugin_manager = register_default_plugins()
    
    # Create pipeline orchestrator
    orchestrator = PipelineOrchestrator(plugin_manager)
    
    # Run pipeline
    try:
        output_paths = orchestrator.run_pipeline(config)
        print(f"Report generation complete! Generated {len(output_paths)} reports:")
        for path in output_paths:
            print(f"  - {path}")
        return 0
    except Exception as e:
        print(f"Error running pipeline: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Step 7: Test the Prototype

Create a test script to validate the prototype:

```python
# /tests/test_prototype.py
import os
import unittest
from compita.core.plugin_manager import PluginManager
from compita.core.pipeline_orchestrator import PipelineOrchestrator
from compita.adapters.csv_parser_adapter import GradebookCSVParserAdapter
from compita.adapters.metrics_processor_adapter import MetricsProcessorAdapter
from compita.adapters.report_generator_adapter import MarkdownReportGeneratorAdapter
from compita.adapters.formatter_adapter import PDFFormatterAdapter

class TestPrototype(unittest.TestCase):
    def setUp(self):
        # Register plugins
        self.plugin_manager = PluginManager()
        self.plugin_manager.register_parser("gradebook", GradebookCSVParserAdapter)
        self.plugin_manager.register_processor("metrics", MetricsProcessorAdapter)
        self.plugin_manager.register_generator("markdown", MarkdownReportGeneratorAdapter)
        self.plugin_manager.register_formatter("pdf", PDFFormatterAdapter)
        
        # Create orchestrator
        self.orchestrator = PipelineOrchestrator(self.plugin_manager)
        
        # Test data
        self.test_date = "25-05-05"
        self.test_assets_dir = "test_assets"
        self.test_output_dir = "test_output"
        
        # Ensure test directories exist
        os.makedirs(f"{self.test_assets_dir}/comptia/{self.test_date}", exist_ok=True)
        os.makedirs(f"{self.test_assets_dir}/processed/{self.test_date}", exist_ok=True)
        os.makedirs(f"{self.test_output_dir}/{self.test_date}/metrics", exist_ok=True)
        os.makedirs(f"{self.test_output_dir}/{self.test_date}/progress_reports", exist_ok=True)
        os.makedirs(f"{self.test_output_dir}/{self.test_date}/executive_reports", exist_ok=True)
    
    def test_pipeline_execution(self):
        # Create test configuration
        config = {
            "parser": {
                "name": "gradebook",
                "args": {
                    "csv_file_path": f"{self.test_assets_dir}/comptia/{self.test_date}/classgradebook.csv",
                    "output_dir": f"{self.test_assets_dir}/processed/{self.test_date}"
                }
            },
            "processor": {
                "name": "metrics",
                "args": {
                    "date_folder": self.test_date,
                    "output_dir": f"{self.test_output_dir}/{self.test_date}/metrics"
                }
            },
            "generator": {
                "name": "markdown",
                "args": {
                    "date": self.test_date,
                    "output_dir": f"{self.test_output_dir}/{self.test_date}/progress_reports"
                }
            },
            "formatter": {
                "name": "pdf",
                "args": {
                    "input_dir": f"{self.test_output_dir}/{self.test_date}/progress_reports",
                    "output_dir": f"{self.test_output_dir}/{self.test_date}/executive_reports"
                }
            }
        }
        
        # Run pipeline (mock execution for testing)
        try:
            # In a real test, we would use mock objects or test data
            # Here we're just testing that the orchestrator runs without errors
            self.orchestrator.run_pipeline(config)
            self.assertTrue(True)  # If we get here, the test passes
        except Exception as e:
            self.fail(f"Pipeline execution failed: {e}")

if __name__ == '__main__':
    unittest.main()
```

### Components to Keep from Existing Codebase

Based on our analysis of the current codebase, we can identify the following components to keep and refactor:

#### 1. CSV Parser Module

**Files to Keep:**
- `/compita/parsers/csv_parser.py`

**Key Functions to Preserve:**
- `parse_csv_to_json()`
- `parse_resource_time_to_json()`
- `parse_study_history_to_json()`
- `categorize_column()`
- `format_seconds_to_time()`

**Refactoring Approach:**
- Extract the core parsing logic into separate classes
- Implement the `BaseCSVParser` interface
- Add support for dynamic column mapping

#### 2. Metrics Collector Module

**Files to Keep:**
- `/compita/collectors/metrics_collector.py`

**Key Classes/Methods to Preserve:**
- `MetricsCollector` class
- `collect_module_metrics()`
- `collect_assessment_metrics()`
- `collect_study_time_metrics()`
- `calculate_summary_metrics()`

**Refactoring Approach:**
- Refactor `MetricsCollector` to implement `BaseProcessor`
- Extract metric calculation strategies into separate classes
- Add support for dynamic metric definitions

#### 3. Report Generator Module

**Files to Keep:**
- `/compita/reports/report_generator.py`
- `/compita/reports/report_formatter.py`

**Key Classes/Methods to Preserve:**
- `ReportFormatter` class
- `format_student_report()`
- `format_class_summary_report()`
- `generate_student_reports()`
- `generate_class_summary()`

**Refactoring Approach:**
- Extract report templates into the template system
- Implement the `BaseGenerator` interface
- Add support for dynamic report sections

#### 4. PDF Converter Module

**Files to Keep:**
- `/compita/converters/markdown_to_pdf.py`

**Key Classes/Methods to Preserve:**
- `MarkdownToPDF` class
- `convert_markdown_to_html()`
- `convert_file()`
- `_enhance_tables()`

**Refactoring Approach:**
- Refactor to implement `BaseFormatter`
- Extract CSS styling into configurable themes
- Add support for additional output formats

### Additional Considerations for the Prototype

1. **Configuration System:**
   - Develop a JSON-based configuration system
   - Support environment-specific configurations
   - Allow for command-line overrides

2. **Logging and Error Handling:**
   - Implement comprehensive logging
   - Add structured error handling
   - Create user-friendly error messages

3. **Testing Framework:**
   - Develop unit tests for all components
   - Create integration tests for the pipeline
   - Set up automated testing with CI/CD

4. **Documentation:**
   - Generate API documentation
   - Create user guides
   - Provide example configurations

## Extended LLM Integration Details

### LLM-Based CSV Schema Inference

The LLM can be used to analyze CSV files and infer their schema, including column types, relationships, and potential metrics:

```python
# Example prompt for CSV schema inference
prompt = f"""
You are an expert data analyst. Analyze the following CSV data sample and provide:

1. Column Definitions:
   - Name
   - Data type (string, number, date, boolean)
   - Description
   - Possible values or range (if applicable)

2. Relationships:
   - Primary key columns
   - Foreign key relationships
   - Hierarchical relationships

3. Potential Metrics:
   - Count metrics
   - Sum metrics
   - Average metrics
   - Rate metrics
   - Custom calculations

CSV Sample:
{csv_sample}

Provide your analysis in JSON format.
"""
```

### LLM-Based Parser Generation

The LLM can generate custom parser code based on the inferred schema:

```python
# Example prompt for parser generation
prompt = f"""
You are an expert Python developer. Create a CSV parser class that implements the BaseCSVParser interface for the following CSV schema:

{json.dumps(schema, indent=2)}

The parser should:
1. Read the CSV file
2. Extract data according to the schema
3. Transform the data into a standardized JSON format
4. Handle edge cases and errors

Use the following base class:

```python
from abc import ABC, abstractmethod

class BaseCSVParser(ABC):
    @abstractmethod
    def parse(self, csv_file_path, output_dir):
        \"\"\"
        Parse a CSV file and convert it to a standardized format.
        
        Args:
            csv_file_path (str): Path to the CSV file
            output_dir (str): Directory to save the output
            
        Returns:
            dict: Parsed data
        \"\"\"
        pass
```

Provide the complete implementation of a custom parser class.
"""
```

### LLM-Based Report Template Generation

The LLM can generate report templates based on the data and metrics:

```python
# Example prompt for report template generation
prompt = f"""
You are an expert in data visualization and reporting. Create a markdown report template for the following data schema and metrics:

Data Schema:
{json.dumps(schema, indent=2)}

Metrics:
{json.dumps(metrics, indent=2)}

The report should include:
1. Executive summary
2. Key metrics overview
3. Detailed sections for each metric category
4. Tables and charts (described in markdown)
5. Recommendations based on the data

Provide the complete markdown template with placeholders for dynamic data.
"""
```

## Conclusion

By following this prototype development method, we can incrementally transform the CompITA Report Generator into a flexible, LLM-powered framework while preserving the valuable components of the existing codebase. The prototype will serve as a proof of concept for the new architecture and provide a foundation for the full implementation of the system.

The prototype will demonstrate:
1. The viability of the modular architecture
2. The integration of LLM for data analysis
3. The flexibility of the plugin system
4. The power of the pipeline orchestrator

This approach minimizes risk by allowing us to test and validate the new architecture while maintaining the functionality of the existing system.

## Additional Components for Prototype Development

After reviewing the complete CompITA codebase, we've identified several additional components that should be included in our prototype to ensure a fully functional system:

### 1. Configuration Management System

The existing configuration system in `/compita/utils/config.py` provides a robust foundation for managing paths, directories, and file naming conventions. We should adapt this for our prototype:

```python
# /compita/core/config_manager.py
import os
import json
from pathlib import Path

class ConfigManager:
    """Configuration manager for the report generator framework."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the configuration."""
        self.base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.assets_dir = self.base_dir / 'assets'
        self.reports_dir = self.base_dir / 'reports'
        self.templates_dir = self.base_dir / 'templates'
        self.static_dir = self.base_dir / 'static'
        self.config_file = self.base_dir / 'config.json'
        
        # Load custom configuration if it exists
        self.custom_config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.custom_config = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {self.config_file}")
    
    def get_processed_data_path(self, date, file_type):
        """Get the path to processed data files."""
        if file_type == 'gradebook':
            return self.assets_dir / 'processed' / date / 'classgradebook.json'
        elif file_type == 'study':
            return self.assets_dir / 'processed' / date / 'studyhistory.json'
        elif file_type == 'resource':
            return self.assets_dir / 'processed' / date / 'timeperresource.json'
        else:
            raise ValueError(f"Unknown file type: {file_type}")
    
    def get_reports_path(self, date, report_type=None):
        """Get the path to report output directories."""
        if report_type == 'progress':
            return self.reports_dir / date / 'progress_reports'
        elif report_type == 'assessment':
            return self.reports_dir / date / 'assessment_reports'
        elif report_type == 'grades':
            return self.reports_dir / date / 'grades_reports'
        elif report_type == 'executive':
            return self.reports_dir / date / 'executive_reports'
        elif report_type == 'metrics':
            return self.reports_dir / date / 'metrics'
        elif report_type == 'student_reports':
            return self.reports_dir / date / 'progress_reports' / 'student_reports'
        elif report_type == 'class_summaries':
            return self.reports_dir / date / 'progress_reports' / 'class_summaries'
        else:
            return self.reports_dir / date
    
    def ensure_directories(self, date):
        """Ensure all necessary directories exist."""
        directories = [
            self.assets_dir / 'processed' / date,
            self.reports_dir / date / 'progress_reports' / 'student_reports',
            self.reports_dir / date / 'progress_reports' / 'class_summaries',
            self.reports_dir / date / 'executive_reports',
            self.reports_dir / date / 'metrics'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_config(self, key, default=None):
        """Get a configuration value."""
        return self.custom_config.get(key, default)
    
    def set_config(self, key, value):
        """Set a configuration value."""
        self.custom_config[key] = value
        
        # Save the configuration
        with open(self.config_file, 'w') as f:
            json.dump(self.custom_config, f, indent=2)
```

### 2. Logging System

The existing logging system in `/compita/utils/logger.py` provides a solid foundation for logging. We should adapt this for our prototype:

```python
# /compita/core/logger.py
import os
import logging
from datetime import datetime
from pathlib import Path

class LoggerFactory:
    """Factory for creating loggers."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name, log_level=logging.INFO):
        """
        Get a logger with the specified name and log level.
        
        Args:
            name (str): The name of the logger.
            log_level (int): The log level to use.
            
        Returns:
            logging.Logger: The configured logger.
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        
        # Create logs directory if it doesn't exist
        logs_dir = Path('logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create file handler
        log_file = logs_dir / f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        # Add file handler to logger
        logger.addHandler(file_handler)
        
        # Store logger
        cls._loggers[name] = logger
        
        return logger
```

### 3. Utility Functions

The existing utility functions in `/compita/utils/helpers.py` provide essential functionality. We should adapt these for our prototype:

```python
# /compita/core/utils.py
import os
import json
import datetime
from pathlib import Path
from typing import Union, Dict, Any, Optional

def format_time_seconds(seconds: int) -> str:
    """
    Format seconds into a human-readable string (e.g., "1h 30m 45s").
    
    Args:
        seconds (int): The number of seconds to format.
        
    Returns:
        str: A formatted time string.
    """
    if seconds is None or seconds == 0:
        return "0s"
    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path (str or Path): The path to the directory.
        
    Returns:
        Path: The path to the directory.
    """
    path = Path(directory_path)
    os.makedirs(path, exist_ok=True)
    return path

def get_timestamp() -> str:
    """
    Get a formatted timestamp for use in filenames.
    
    Returns:
        str: A formatted timestamp.
    """
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def load_json(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """
    Load JSON data from a file.
    
    Args:
        file_path (str or Path): The path to the JSON file.
        
    Returns:
        dict: The loaded JSON data or None if the file doesn't exist or is invalid.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON from {file_path}: {e}")
        return None

def save_json(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data (dict): The data to save.
        file_path (str or Path): The path to the JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the data
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving JSON to {file_path}: {e}")
        return False

def normalize_student_name(name: str) -> str:
    """
    Normalize a student name by stripping whitespace.
    
    Args:
        name (str): The student name to normalize.
        
    Returns:
        str: The normalized student name.
    """
    if not name:
        return ""
    
    # Strip whitespace
    normalized = name.strip()
    
    return normalized
```

### 4. HTML Templates

The existing HTML templates in `/compita/templates/` are essential for PDF generation. We should include these in our prototype:

```python
# /compita/core/template_manager.py
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateManager:
    """Manager for HTML templates."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TemplateManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the template manager."""
        self.template_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'templates'
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
    
    def get_template(self, template_name):
        """
        Get a template by name.
        
        Args:
            template_name (str): The name of the template.
            
        Returns:
            jinja2.Template: The template.
        """
        return self.env.get_template(template_name)
    
    def render_template(self, template_name, **kwargs):
        """
        Render a template with the specified context.
        
        Args:
            template_name (str): The name of the template.
            **kwargs: The template context.
            
        Returns:
            str: The rendered template.
        """
        template = self.get_template(template_name)
        return template.render(**kwargs)
```

### 5. Markdown Formatter Adapter

The existing markdown formatter in `/compita/formatters/markdown_formatter.py` provides essential functionality for report generation. We should adapt this for our prototype:

```python
# /compita/adapters/markdown_formatter_adapter.py
from compita.core.base_generator import BaseGenerator
from compita.formatters.markdown_formatter import format_student_report, format_class_summary
from compita.core.utils import save_json, ensure_directory
from pathlib import Path

class MarkdownFormatterAdapter(BaseGenerator):
    """Adapter for the markdown formatter."""
    
    def generate(self, metrics_data, output_dir):
        """
        Generate markdown reports from metrics data.
        
        Args:
            metrics_data (dict): The metrics data.
            output_dir (str): The output directory.
            
        Returns:
            list: Paths to the generated reports.
        """
        # Ensure the output directory exists
        ensure_directory(output_dir)
        
        # Create student reports directory
        student_reports_dir = Path(output_dir) / 'student_reports'
        ensure_directory(student_reports_dir)
        
        # Create class summaries directory
        class_summaries_dir = Path(output_dir) / 'class_summaries'
        ensure_directory(class_summaries_dir)
        
        report_paths = []
        
        # Generate student reports
        for student_name, student_data in metrics_data.items():
            # Format the student report
            report_content = format_student_report(student_name, student_data, metrics_data)
            
            # Save the report
            safe_name = student_name.replace(' ', '_').replace(',', '').strip()
            report_path = student_reports_dir / f"student_{safe_name}_report.md"
            
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            report_paths.append(str(report_path))
        
        # Generate class summary
        report_content = format_class_summary(metrics_data)
        report_path = class_summaries_dir / "class_summary_report.md"
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        report_paths.append(str(report_path))
        
        return report_paths
```

### 6. Complete Adapter Classes

Based on our review of the codebase, we need to implement the remaining adapter classes for the prototype:

```python
# /compita/adapters/metrics_processor_adapter.py
from compita.core.base_processor import BaseProcessor
from compita.collectors.metrics_collector import MetricsCollector
from compita.core.utils import save_json, ensure_directory
from pathlib import Path

class MetricsProcessorAdapter(BaseProcessor):
    """Adapter for the metrics collector."""
    
    def process(self, parsed_data, date_folder, output_dir):
        """
        Process parsed data into metrics.
        
        Args:
            parsed_data (dict): The parsed data.
            date_folder (str): The date folder.
            output_dir (str): The output directory.
            
        Returns:
            dict: The processed metrics.
        """
        # Create metrics collector
        collector = MetricsCollector(date_folder)
        
        # Collect metrics
        metrics_file = collector.collect_all_metrics()
        
        # Load metrics
        with open(metrics_file, 'r') as f:
            import json
            metrics = json.load(f)
        
        return metrics
```

```python
# /compita/adapters/report_generator_adapter.py
from compita.core.base_generator import BaseGenerator
from compita.reports.report_generator import generate_student_reports, generate_class_summary
from compita.core.utils import ensure_directory
from pathlib import Path

class MarkdownReportGeneratorAdapter(BaseGenerator):
    """Adapter for the markdown report generator."""
    
    def generate(self, metrics_data, date, output_dir):
        """
        Generate reports from metrics data.
        
        Args:
            metrics_data (dict): The metrics data.
            date (str): The date in YY-MM-DD format.
            output_dir (str): The output directory.
            
        Returns:
            list: Paths to the generated reports.
        """
        # Ensure the output directory exists
        ensure_directory(output_dir)
        
        # Create student reports directory
        student_reports_dir = Path(output_dir) / 'student_reports'
        ensure_directory(student_reports_dir)
        
        # Create class summaries directory
        class_summaries_dir = Path(output_dir) / 'class_summaries'
        ensure_directory(class_summaries_dir)
        
        # Save metrics data to a temporary file
        import json
        import tempfile
        import os
        
        temp_dir = tempfile.mkdtemp()
        metrics_file = os.path.join(temp_dir, 'metrics.json')
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        # Generate student reports
        student_report_paths = generate_student_reports(date, output_dir=str(student_reports_dir))
        
        # Generate class summary
        class_summary_paths = generate_class_summary(date, output_dir=str(class_summaries_dir))
        
        # Clean up
        os.remove(metrics_file)
        os.rmdir(temp_dir)
        
        return student_report_paths + class_summary_paths
```

```python
# /compita/adapters/formatter_adapter.py
from compita.core.base_formatter import BaseFormatter
from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
from compita.core.utils import ensure_directory
from pathlib import Path

class PDFFormatterAdapter(BaseFormatter):
    """Adapter for the PDF formatter."""
    
    def format(self, report_data, input_dir, output_dir):
        """
        Format reports into PDFs.
        
        Args:
            report_data (list): Paths to the report files.
            input_dir (str): The input directory containing markdown files.
            output_dir (str): The output directory for PDF files.
            
        Returns:
            list: Paths to the generated PDF files.
        """
        # Ensure the output directory exists
        ensure_directory(output_dir)
        
        # Convert markdown to PDF
        pdf_paths = convert_markdown_to_pdf(input_dir, output_dir)
        
        return pdf_paths
```

### 7. Updated Pipeline Orchestrator

Based on our review, we need to update the pipeline orchestrator to handle the complete workflow:

```python
# /compita/core/pipeline_orchestrator.py
from compita.core.plugin_manager import PluginManager
from compita.core.config_manager import ConfigManager
from compita.core.logger import LoggerFactory

class PipelineOrchestrator:
    """Orchestrator for the report generation pipeline."""
    
    def __init__(self, plugin_manager=None):
        """
        Initialize the pipeline orchestrator.
        
        Args:
            plugin_manager (PluginManager): The plugin manager.
        """
        self.plugin_manager = plugin_manager or PluginManager()
        self.config_manager = ConfigManager()
        self.logger = LoggerFactory.get_logger("pipeline_orchestrator")
    
    def run_pipeline(self, config):
        """
        Run the report generation pipeline based on configuration.
        
        Args:
            config (dict): Pipeline configuration
                {
                    "parser": {"name": "gradebook", "args": {...}},
                    "processor": {"name": "metrics", "args": {...}},
                    "generator": {"name": "markdown", "args": {...}},
                    "formatter": {"name": "pdf", "args": {...}}
                }
        
        Returns:
            list: Paths to the generated reports
        """
        self.logger.info("Starting pipeline execution")
        
        # Ensure directories exist
        if "date" in config.get("parser", {}).get("args", {}):
            date = config["parser"]["args"]["date"]
            self.config_manager.ensure_directories(date)
        
        # Get components from plugin manager
        parser_name = config["parser"]["name"]
        processor_name = config["processor"]["name"]
        generator_name = config["generator"]["name"]
        formatter_name = config["formatter"]["name"]
        
        self.logger.info(f"Using parser: {parser_name}")
        self.logger.info(f"Using processor: {processor_name}")
        self.logger.info(f"Using generator: {generator_name}")
        self.logger.info(f"Using formatter: {formatter_name}")
        
        parser_class = self.plugin_manager.get_parser(parser_name)
        processor_class = self.plugin_manager.get_processor(processor_name)
        generator_class = self.plugin_manager.get_generator(generator_name)
        formatter_class = self.plugin_manager.get_formatter(formatter_name)
        
        if not all([parser_class, processor_class, generator_class, formatter_class]):
            missing = []
            if not parser_class: missing.append(f"parser '{parser_name}'")
            if not processor_class: missing.append(f"processor '{processor_name}'")
            if not generator_class: missing.append(f"generator '{generator_name}'")
            if not formatter_class: missing.append(f"formatter '{formatter_name}'")
            error_msg = f"Missing components: {', '.join(missing)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Initialize components
        parser = parser_class()
        processor = processor_class()
        generator = generator_class()
        formatter = formatter_class()
        
        # Run pipeline
        try:
            self.logger.info("Parsing data")
            parsed_data = parser.parse(**config["parser"]["args"])
            
            self.logger.info("Processing data")
            processed_data = processor.process(parsed_data, **config["processor"]["args"])
            
            self.logger.info("Generating reports")
            report_data = generator.generate(processed_data, **config["generator"]["args"])
            
            self.logger.info("Formatting reports")
            output_paths = formatter.format(report_data, **config["formatter"]["args"])
            
            self.logger.info(f"Pipeline execution complete. Generated {len(output_paths)} reports.")
            return output_paths
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            raise
```

### 8. Complete Project Structure

Based on our review, here is the complete project structure for the prototype:

```
compita/
├── __init__.py
├── adapters/
│   ├── __init__.py
│   ├── csv_parser_adapter.py
│   ├── formatter_adapter.py
│   ├── markdown_formatter_adapter.py
│   ├── metrics_processor_adapter.py
│   └── report_generator_adapter.py
├── cli/
│   ├── __init__.py
│   ├── commands.py
│   └── new_cli.py
├── collectors/
│   ├── __init__.py
│   └── metrics_collector.py
├── converters/
│   ├── __init__.py
│   └── markdown_to_pdf.py
├── core/
│   ├── __init__.py
│   ├── base_formatter.py
│   ├── base_generator.py
│   ├── base_parser.py
│   ├── base_processor.py
│   ├── config_manager.py
│   ├── logger.py
│   ├── pipeline_orchestrator.py
│   ├── plugin_manager.py
│   ├── template_manager.py
│   └── utils.py
├── formatters/
│   ├── __init__.py
│   └── markdown_formatter.py
├── llm/
│   ├── __init__.py
│   ├── csv_analyzer.py
│   ├── llm_service.py
│   └── parser_generator.py
├── parsers/
│   ├── __init__.py
│   └── csv_parser.py
├── reports/
│   ├── __init__.py
│   ├── report_formatter.py
│   └── report_generator.py
└── templates/
    ├── assets/
    ├── base.html
    ├── class_summary.html
    └── student_report.html
```

This structure incorporates all the essential components from the existing codebase while introducing the new modular architecture. The prototype will be able to leverage the existing functionality while providing a foundation for the new features.

## Updated Prototype Development Plan

Based on our review of the CompITA codebase, we've updated the prototype development plan to include the additional components:

1. **Create Core Directory Structure**: Set up the new directory structure with the core, adapters, and llm directories.

2. **Implement Core Abstract Classes**: Create the base classes for parsers, processors, generators, and formatters.

3. **Implement Core Utilities**: Adapt the existing utility functions, configuration management, and logging system.

4. **Create Adapter Classes**: Implement adapters for the existing CSV parser, metrics collector, report generator, and PDF converter.

5. **Implement Plugin Manager**: Create the plugin manager for registering and retrieving components.

6. **Implement Pipeline Orchestrator**: Create the orchestrator for managing the flow of data through the pipeline.

7. **Create Configuration-Based CLI**: Develop a new CLI that uses the pipeline orchestrator and configuration.

8. **Implement Basic LLM Integration**: Create a simple LLM service and CSV analyzer for testing.

9. **Test the Prototype**: Validate the prototype with existing data.

This updated plan ensures that we leverage all the valuable components of the existing codebase while introducing the new modular architecture. The prototype will serve as a proof of concept for the full transformation of the CompITA Report Generator into a flexible, LLM-powered framework.

```
{{ ... }}

```

Follow these instructions to make the following change to my code document.

Instruction: Enhancing the transformation plan with additional details based on the review of collectors, converters, formatters, parsers, and reports directories. Fixing the incomplete edit from the previous attempt.

Code Edit:
```
{{ ... }}

## Components to Keep from Existing Codebase

The following components from the existing codebase should be preserved and adapted for the new architecture:

### Configuration Management

The existing configuration system from `/compita/utils/config.py` provides a solid foundation for managing paths, directories, and file naming conventions. We'll adapt this for our prototype.

```python
class Config:
    def __init__(self):
        self.base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.assets_dir = self.base_dir / 'assets'
        self.reports_dir = self.base_dir / 'reports'
        self.templates_dir = self.base_dir / 'templates'
        self.static_dir = self.base_dir / 'static'
        
    def get_processed_data_path(self, date, file_type):
        # Implementation for getting processed data paths
        
    def get_reports_path(self, date, report_type=None):
        # Implementation for getting report paths
        
    def ensure_directories(self, date):
        # Implementation for ensuring directories exist
```

### Logging System

The existing logging system from `/compita/utils/logger.py` provides comprehensive logging capabilities. We'll adapt this for our prototype.

```python
def setup_logger(name, log_level=logging.INFO):
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create file handler
    log_file = f"logs/{name}_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger
```

### Utility Functions

Essential utility functions from `/compita/utils/helpers.py` should be preserved, including:

```python
def format_time_seconds(seconds: int) -> str:
    """Format seconds into a human-readable string (e.g., "1h 30m 45s")."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def ensure_directory(directory_path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory_path, exist_ok=True)
```

### HTML Templates

The existing HTML templates in `/compita/templates/` are essential for PDF generation and should be preserved.

### CSV Parser Functionality

The CSV parsing functionality in `/compita/parsers/csv_parser.py` provides robust parsing capabilities for various CSV formats. Key functions to adapt include:

```python
def parse_csv_to_json(csv_file_path: str, output_dir: str):
    """Parse a CSV file containing student assessment data and convert it to JSON format."""
    
def parse_resource_time_to_json(csv_file_path: str, output_dir: str):
    """Parse a CSV file containing time spent per resource by students and convert it to JSON format."""
    
def parse_study_history_to_json(csv_file_path: str, output_dir: str):
    """Parse a CSV file containing student study history data and convert it to JSON format."""
```

### Metrics Collection

The metrics collection functionality in `/compita/collectors/metrics_collector.py` provides comprehensive metrics gathering and processing. Key methods to adapt include:

```python
def collect_module_metrics(self):
    """Collect metrics from the module completion data."""
    
def collect_assessment_metrics(self):
    """Collect metrics from the assessment grades data."""
    
def collect_study_time_metrics(self):
    """Collect metrics from the study time data."""
    
def calculate_summary_metrics(self):
    """Calculate summary metrics for each student."""
```

### Report Formatting

The report formatting functionality in `/compita/formatters/markdown_formatter.py` provides robust formatting for student and class reports. Key functions to adapt include:

```python
def format_student_report(student_name: str, student_data: Dict[str, Any], metrics_data: Dict[str, Any]) -> str:
    """Format student data into a markdown report."""
    
def format_class_summary(metrics_data: Dict[str, Any]) -> str:
    """Format class metrics data into a markdown report."""
```

### PDF Converter Module

The PDF converter module in `/compita/converters/markdown_to_pdf.py` provides robust PDF generation capabilities. Key methods to adapt include:

```python
def convert_markdown_to_html(self, markdown_content, title):
    """Convert markdown content to HTML."""
    
def convert_html_to_pdf(self, html_content, output_path):
    """Convert HTML content to PDF."""
    
def convert_file(self, input_path, output_path=None, title=None):
    """Convert a markdown file to PDF."""
```

### Flexible Report Generation

The flexible report generation functionality in `/compita/reports/` provides specialized report generation capabilities. Key modules to adapt include:

- `flexible_module.py`: Generates module completion reports
- `flexible_assessment.py`: Generates assessment reports
- `flexible_grades.py`: Generates grades reports
- `report_generator.py`: Coordinates the entire reporting process

## Enhanced Adapter Classes

Based on our review of the existing codebase, we'll create the following adapter classes to integrate with our new architecture:

### CSV Parser Adapter

```python
class CSVParserAdapter(BaseCSVParser):
    """Adapter for the existing CSV parser."""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = setup_logger("csv_parser_adapter")
        
    def parse(self, file_path, output_path=None):
        """Parse a CSV file and return the parsed data."""
        self.logger.info(f"Parsing CSV file: {file_path}")
        
        # Determine the parser type based on the file name
        if "gradebook" in file_path.lower():
            return self._parse_gradebook(file_path, output_path)
        elif "studyhistory" in file_path.lower() or "classstudyhistory" in file_path.lower():
            return self._parse_study_history(file_path, output_path)
        elif "timeperresource" in file_path.lower():
            return self._parse_resource_time(file_path, output_path)
        else:
            self.logger.error(f"Unknown CSV file type: {file_path}")
            return None
            
    def _parse_gradebook(self, file_path, output_path):
        """Parse a gradebook CSV file."""
        from compita.parsers.csv_parser import parse_csv_to_json
        return parse_csv_to_json(file_path, output_path or self.config.get_processed_data_path())
        
    def _parse_study_history(self, file_path, output_path):
        """Parse a study history CSV file."""
        from compita.parsers.csv_parser import parse_study_history_to_json
        return parse_study_history_to_json(file_path, output_path or self.config.get_processed_data_path())
        
    def _parse_resource_time(self, file_path, output_path):
        """Parse a resource time CSV file."""
        from compita.parsers.csv_parser import parse_resource_time_to_json
        return parse_resource_time_to_json(file_path, output_path or self.config.get_processed_data_path())
```

### Metrics Processor Adapter

```python
class MetricsProcessorAdapter(BaseMetricsProcessor):
    """Adapter for the existing metrics processor."""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = setup_logger("metrics_processor_adapter")
        
    def process(self, data, output_path=None):
        """Process metrics from the provided data."""
        self.logger.info("Processing metrics")
        
        # Extract date from the data or use current date
        date = data.get("date", datetime.now().strftime("%y-%m-%d"))
        
        # Use the existing metrics collector
        from compita.collectors.metrics_collector import collect_metrics
        metrics = collect_metrics(date)
        
        # Save metrics to the output path if provided
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(metrics, f, indent=2)
                
        return metrics
```

### Report Generator Adapter

```python
class ReportGeneratorAdapter(BaseReportGenerator):
    """Adapter for the existing report generator."""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = setup_logger("report_generator_adapter")
        
    def generate(self, metrics_data, output_path=None, report_type="student", entity_name=None):
        """Generate a report from the provided metrics data."""
        self.logger.info(f"Generating {report_type} report")
        
        # Extract date from the metrics data or use current date
        date = metrics_data.get("date", datetime.now().strftime("%y-%m-%d"))
        
        # Determine output path if not provided
        if not output_path:
            if report_type == "student":
                output_path = self.config.get_reports_path(date, "student_reports")
            elif report_type == "class":
                output_path = self.config.get_reports_path(date, "class_summaries")
            else:
                output_path = self.config.get_reports_path(date)
                
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Use the existing report generator
        from compita.formatters.markdown_formatter import format_student_report, format_class_summary
        
        if report_type == "student":
            # Generate student report
            if entity_name:
                # Get student data from metrics
                student_data = None
                if 'student_metrics' in metrics_data and entity_name in metrics_data['student_metrics']:
                    student_data = metrics_data['student_metrics'][entity_name]
                elif entity_name in metrics_data:
                    student_data = metrics_data[entity_name]
                    
                if student_data:
                    # Format student name for filename
                    student_filename = entity_name.replace(', ', '_').replace(' ', '_')
                    output_file = os.path.join(output_path, f"student_{student_filename}.md")
                    
                    # Format and save the report
                    report_content = format_student_report(entity_name, student_data, metrics_data)
                    with open(output_file, 'w') as f:
                        f.write(report_content)
                        
                    return output_file
                else:
                    self.logger.error(f"No data found for student: {entity_name}")
                    return None
            else:
                # Generate reports for all students
                output_files = []
                for student_name, student_data in metrics_data.items():
                    if isinstance(student_data, dict) and 'modules' in student_data:
                        # Format student name for filename
                        student_filename = student_name.replace(', ', '_').replace(' ', '_')
                        output_file = os.path.join(output_path, f"student_{student_filename}.md")
                        
                        # Format and save the report
                        report_content = format_student_report(student_name, student_data, metrics_data)
                        with open(output_file, 'w') as f:
                            f.write(report_content)
                            
                        output_files.append(output_file)
                        
                return output_files
        elif report_type == "class":
            # Generate class summary report
            output_file = os.path.join(output_path, "class_summary.md")
            
            # Format and save the report
            report_content = format_class_summary(metrics_data)
            with open(output_file, 'w') as f:
                f.write(report_content)
                
            return output_file
        else:
            self.logger.error(f"Unknown report type: {report_type}")
            return None
```

### PDF Formatter Adapter

```python
class PDFFormatterAdapter(BaseOutputFormatter):
    """Adapter for the existing PDF formatter."""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = setup_logger("pdf_formatter_adapter")
        
    def format(self, input_path, output_path=None, format_type="pdf"):
        """Format the input file to the specified format."""
        self.logger.info(f"Formatting {input_path} to {format_type}")
        
        if format_type.lower() != "pdf":
            self.logger.error(f"Unsupported format type: {format_type}")
            return None
            
        # Determine output path if not provided
        if not output_path:
            output_path = input_path.replace(".md", ".pdf")
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Use the existing markdown to PDF converter
        from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
        
        # Get the input directory and create a temporary output directory
        input_dir = os.path.dirname(input_path)
        output_dir = os.path.dirname(output_path)
        
        # Convert the file
        pdf_files = convert_markdown_to_pdf(input_dir, output_dir)
        
        # Return the path to the generated PDF file
        for pdf_file in pdf_files:
            if os.path.basename(pdf_file).replace(".pdf", ".md") == os.path.basename(input_path):
                return pdf_file
                
        return None
```

## Enhanced Pipeline Orchestrator

Based on our review of the existing codebase, we'll enhance the pipeline orchestrator to handle the complete workflow:

```python
class PipelineOrchestrator:
    """Orchestrates the entire pipeline from CSV parsing to PDF generation."""
    
    def __init__(self, config, plugin_manager):
        self.config = config
        self.plugin_manager = plugin_manager
        self.logger = setup_logger("pipeline_orchestrator")
        
    def run(self, csv_files, output_dir, report_types=None, entity_names=None, llm_service=None):
        """Run the complete pipeline."""
        self.logger.info("Starting pipeline execution")
        
        # Step 1: Parse CSV files
        parsed_data = self._parse_csv_files(csv_files)
        if not parsed_data:
            self.logger.error("CSV parsing failed. Aborting pipeline.")
            return None
            
        # Step 2: Process metrics
        metrics_data = self._process_metrics(parsed_data)
        if not metrics_data:
            self.logger.error("Metrics processing failed. Aborting pipeline.")
            return None
            
        # Step 3: Generate reports
        report_files = self._generate_reports(metrics_data, output_dir, report_types, entity_names)
        if not report_files:
            self.logger.error("Report generation failed. Aborting pipeline.")
            return None
            
        # Step 4: Format reports to PDF
        pdf_files = self._format_reports(report_files, output_dir)
        if not pdf_files:
            self.logger.error("PDF formatting failed. Aborting pipeline.")
            return None
            
        self.logger.info("Pipeline execution completed successfully")
        return pdf_files
        
    def _parse_csv_files(self, csv_files):
        """Parse CSV files using the appropriate parser."""
        parsed_data = {}
        
        # Get the CSV parser from the plugin manager
        csv_parser = self.plugin_manager.get_plugin("csv_parser")
        if not csv_parser:
            self.logger.error("No CSV parser plugin found")
            return None
            
        # Parse each CSV file
        for csv_file in csv_files:
            file_data = csv_parser.parse(csv_file)
            if file_data:
                parsed_data[os.path.basename(csv_file)] = file_data
                
        return parsed_data
        
    def _process_metrics(self, parsed_data):
        """Process metrics from the parsed data."""
        # Get the metrics processor from the plugin manager
        metrics_processor = self.plugin_manager.get_plugin("metrics_processor")
        if not metrics_processor:
            self.logger.error("No metrics processor plugin found")
            return None
            
        # Process the metrics
        return metrics_processor.process(parsed_data)
        
    def _generate_reports(self, metrics_data, output_dir, report_types=None, entity_names=None):
        """Generate reports from the metrics data."""
        # Get the report generator from the plugin manager
        report_generator = self.plugin_manager.get_plugin("report_generator")
        if not report_generator:
            self.logger.error("No report generator plugin found")
            return None
            
        # Generate reports
        report_files = []
        
        # Default to all report types if none specified
        if not report_types:
            report_types = ["student", "class"]
            
        # Generate reports for each type
        for report_type in report_types:
            if report_type == "student":
                if entity_names:
                    # Generate reports for specific students
                    for entity_name in entity_names:
                        report_file = report_generator.generate(metrics_data, output_dir, report_type, entity_name)
                        if report_file:
                            report_files.append(report_file)
                else:
                    # Generate reports for all students
                    student_reports = report_generator.generate(metrics_data, output_dir, report_type)
                    if student_reports:
                        report_files.extend(student_reports)
            elif report_type == "class":
                # Generate class summary report
                class_report = report_generator.generate(metrics_data, output_dir, report_type)
                if class_report:
                    report_files.append(class_report)
                    
        return report_files
        
    def _format_reports(self, report_files, output_dir):
        """Format reports to PDF."""
        # Get the PDF formatter from the plugin manager
        pdf_formatter = self.plugin_manager.get_plugin("pdf_formatter")
        if not pdf_formatter:
            self.logger.error("No PDF formatter plugin found")
            return None
            
        # Format each report to PDF
        pdf_files = []
        for report_file in report_files:
            pdf_file = pdf_formatter.format(report_file, None, "pdf")
            if pdf_file:
                pdf_files.append(pdf_file)
                
        return pdf_files
```

## Complete Project Structure

Based on our comprehensive review of the existing codebase, here's the complete project structure for our prototype:

```
compita_llm/
├── compita/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract base classes
│   │   ├── config.py               # Configuration management
│   │   ├── logger.py               # Logging system
│   │   ├── plugin_manager.py       # Plugin management system
│   │   └── pipeline.py             # Pipeline orchestration
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── csv_parser_adapter.py   # Adapter for existing CSV parser
│   │   ├── metrics_processor_adapter.py  # Adapter for existing metrics processor
│   │   ├── report_generator_adapter.py   # Adapter for existing report generator
│   │   └── pdf_formatter_adapter.py      # Adapter for existing PDF formatter
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── service.py              # LLM service integration
│   │   ├── csv_analyzer.py         # CSV analysis using LLM
│   │   ├── parser_generator.py     # Dynamic parser generation using LLM
│   │   └── report_template_generator.py  # Report template generation using LLM
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base_parser.py          # Base parser implementation
│   │   ├── dynamic_parser.py       # Dynamic parser implementation
│   │   └── utils.py                # Parser utilities
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── base_processor.py       # Base metrics processor implementation
│   │   ├── dynamic_processor.py    # Dynamic metrics processor implementation
│   │   └── utils.py                # Processor utilities
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── base_generator.py       # Base report generator implementation
│   │   ├── dynamic_generator.py    # Dynamic report generator implementation
│   │   └── utils.py                # Generator utilities
│   ├── formatters/
│   │   ├── __init__.py
│   │   ├── base_formatter.py       # Base output formatter implementation
│   │   ├── markdown_formatter.py   # Markdown formatter implementation
│   │   ├── pdf_formatter.py        # PDF formatter implementation
│   │   └── utils.py                # Formatter utilities
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── base.html               # Base HTML template
│   │   ├── class_summary.html      # Class summary template
│   │   └── student_report.html     # Student report template
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py              # Helper functions
│       └── file_utils.py           # File utility functions
├── cli/
│   ├── __init__.py
│   ├── commands.py                 # CLI commands
│   └── utils.py                    # CLI utilities
├── config/
│   ├── __init__.py
│   ├── default.json                # Default configuration
│   └── schema.json                 # Configuration schema
├── tests/
│   ├── __init__.py
│   ├── test_core/                  # Tests for core components
│   ├── test_adapters/              # Tests for adapter components
│   ├── test_llm/                   # Tests for LLM components
│   ├── test_parsers/               # Tests for parser components
│   ├── test_processors/            # Tests for processor components
│   ├── test_generators/            # Tests for generator components
│   ├── test_formatters/            # Tests for formatter components
│   └── test_cli/                   # Tests for CLI components
├── docs/
│   ├── __init__.py
│   ├── api/                        # API documentation
│   ├── user_guide/                 # User guide
│   └── developer_guide/            # Developer guide
├── examples/
│   ├── __init__.py
│   ├── basic_usage.py              # Basic usage example
│   ├── custom_parser.py            # Custom parser example
│   └── llm_integration.py          # LLM integration example
├── setup.py                        # Package setup script
├── requirements.txt                # Package dependencies
├── README.md                       # Project README
└── LICENSE                         # Project license
```

This project structure incorporates all the essential components from the existing codebase while introducing the new modular architecture. The adapters directory contains adapter classes that integrate the existing functionality with the new architecture, allowing for a smooth transition.

{{ ... }}

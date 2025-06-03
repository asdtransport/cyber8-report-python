"""
Interactive CLI for the CompITA report generator.
"""
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable

# Add parent directory to path to allow importing from the package
sys.path.append(str(Path(__file__).parent.parent.parent))


class InteractiveCLI:
    """Interactive CLI for the Cyber8 report generator."""

    def __init__(self):
        """Initialize the interactive CLI."""
        self.commands = {
            "1": {
                "name": "Generate All Reports",
                "description": "Generate all reports for a specific date",
                "function": self.run_generate_all,
                "options": ["date", "assets_dir", "output_dir"]
            },
            "2": {
                "name": "Flexible Module Report",
                "description": "Generate flexible module report",
                "function": self.run_flexible_module,
                "options": ["date", "all_modules", "subset_modules", "exclude_modules", 
                            "output_prefix", "count_partial", "assets_dir", "output_dir"]
            },
            "3": {
                "name": "Flexible Assessment Report",
                "description": "Generate flexible assessment report",
                "function": self.run_flexible_assessment,
                "options": ["date", "assessment_types", "output_prefix", "assets_dir", "output_dir"]
            },
            "4": {
                "name": "Flexible Grades Report",
                "description": "Generate flexible grades report",
                "function": self.run_flexible_grades,
                "options": ["date", "grade_categories", "grade_weights", "output_prefix", "assets_dir", "output_dir"]
            },
            "5": {
                "name": "Markdown to PDF Conversion",
                "description": "Convert markdown files to PDF",
                "function": self.run_markdown_to_pdf,
                "options": ["input_dir", "output_dir"]
            },
            "6": {
                "name": "Student Reports",
                "description": "Generate student reports",
                "function": self.run_student_reports,
                "options": ["date", "output_dir", "assets_dir"]
            },
            "7": {
                "name": "Class Summary",
                "description": "Generate class summary report",
                "function": self.run_class_summary,
                "options": ["date", "output_dir", "assets_dir"]
            },
            "8": {
                "name": "CSV Module Report",
                "description": "Generate CSV report for a specific module",
                "function": self.run_csv_module_report,
                "options": ["date", "module", "current_module", "assets_dir", "output_dir"]
            },
            "9": {
                "name": "CSV Student Report",
                "description": "Generate CSV report for a specific student",
                "function": self.run_csv_student_report,
                "options": ["date", "student", "assets_dir", "output_dir"]
            },
            "10": {
                "name": "CSV Class Report",
                "description": "Generate CSV report for the entire class",
                "function": self.run_csv_class_report,
                "options": ["date", "current_module", "assets_dir", "output_dir"]
            },
            "11": {
                "name": "Excel Report",
                "description": "Generate Excel report with multiple sheets",
                "function": self.run_excel_report,
                "options": ["date", "current_module", "assets_dir", "output_dir"]
            },
            "12": {
                "name": "All CSV Reports",
                "description": "Generate all CSV reports (modules, students, class, Excel)",
                "function": self.run_all_csv_reports,
                "options": ["date", "current_module", "assets_dir", "output_dir"]
            },
            "q": {
                "name": "Quit",
                "description": "Exit the application",
                "function": self.quit,
                "options": []
            }
        }
        
        self.option_descriptions = {
            "date": "Date in YY-MM-DD format (e.g., 25-05-05)",
            "all_modules": "List of module numbers to include in the overall analysis (e.g., 1 2 3)",
            "subset_modules": "List of module numbers to include in the subset analysis (e.g., 1 2)",
            "exclude_modules": "List of module numbers to exclude from the overall analysis (e.g., 4 5)",
            "output_prefix": "Prefix for the output files (e.g., custom_report)",
            "count_partial": "Count partial completions as fully completed (yes/no)",
            "assessment_types": "List of assessment types to include (e.g., quiz exam project)",
            "grade_categories": "List of grade categories to include (e.g., quiz exam project)",
            "grade_weights": "List of grade weights (e.g., 0.3 0.4 0.3)",
            "input_dir": "Input directory containing markdown files",
            "output_dir": "Output directory for PDF files",
            "module": "Module number to generate the report for (e.g., 1)",
            "student": "Student name to generate the report for (e.g., Smith, John)",
            "current_module": "Current module being taught (used for calculating modules behind, default: 7)",
            "assets_dir": "Directory containing assets (e.g., images, templates)",
        }
        
        # Default values
        today = datetime.now().strftime("%y-%m-%d")
        self.default_values = {
            "date": today,
            "count_partial": "no",
            "output_prefix": "report",
            "output_dir": f"reports/{today}/progress_reports/student_reports",
            "input_dir": f"reports/{today}/progress_reports",
            "current_module": "7",
            "assets_dir": "assets"
        }

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("Cyber8 Report Generator - Interactive CLI".center(60))
        print("=" * 60)
        print("Available commands:")
        
        for key, command in self.commands.items():
            print(f"{key}. {command['name']} - {command['description']}")
        
        print("=" * 60)

    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """
        Get input from the user with an optional default value.
        
        Args:
            prompt: The prompt to display to the user
            default: The default value to use if the user enters nothing
            
        Returns:
            The user input or the default value
        """
        try:
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                return user_input if user_input else default
            else:
                return input(f"{prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted. Exiting...")
            sys.exit(0)

    def get_list_input(self, prompt: str) -> List[str]:
        """
        Get a list of inputs from the user.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            A list of user inputs
        """
        user_input = self.get_input(f"{prompt} (space-separated)")
        return user_input.split() if user_input else []

    def get_boolean_input(self, prompt: str, default: bool = False) -> bool:
        """
        Get a boolean input from the user.
        
        Args:
            prompt: The prompt to display to the user
            default: The default value to use if the user enters nothing
            
        Returns:
            A boolean value
        """
        default_str = "yes" if default else "no"
        user_input = self.get_input(f"{prompt} (yes/no)", default_str).lower()
        return user_input in ["yes", "y", "true", "t", "1"]

    def get_option_value(self, option: str) -> Any:
        """
        Get the value for a specific option.
        
        Args:
            option: The option to get the value for
            
        Returns:
            The value for the option
        """
        description = self.option_descriptions.get(option, option)
        default = self.default_values.get(option, None)
        
        if option in ["all_modules", "subset_modules", "exclude_modules", 
                      "assessment_types", "grade_categories"]:
            return self.get_list_input(f"Enter {description}")
        elif option == "grade_weights":
            weights_str = self.get_list_input(f"Enter {description}")
            return [float(w) for w in weights_str] if weights_str else []
        elif option == "count_partial":
            return self.get_boolean_input(f"Enter {description}", default == "yes")
        elif option == "module":
            module_str = self.get_input(f"Enter {description}")
            return int(module_str) if module_str else None
        elif option == "current_module":
            current_module_str = self.get_input(f"Enter {description}", default)
            return int(current_module_str) if current_module_str else 7
        else:
            return self.get_input(f"Enter {description}", default)

    def collect_options(self, options: List[str]) -> Dict[str, Any]:
        """
        Collect option values from the user.
        
        Args:
            options: The options to collect values for
            
        Returns:
            A dictionary of option values
        """
        print("\nPlease enter the following options:")
        option_values = {}
        
        for option in options:
            option_values[option] = self.get_option_value(option)
            
        return option_values

    def confirm_run(self, command_name: str, options: Dict[str, Any]) -> bool:
        """
        Confirm that the user wants to run the command.
        
        Args:
            command_name: The name of the command
            options: The options for the command
            
        Returns:
            True if the user confirms, False otherwise
        """
        print("\nCommand Summary:")
        print(f"Command: {command_name}")
        print("Options:")
        
        for option, value in options.items():
            print(f"  {option}: {value}")
            
        return self.get_boolean_input("\nDo you want to run this command?", True)

    def run_generate_all(self, options: Dict[str, Any]) -> int:
        """
        Run the generate-all command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.cli.commands import generate_all
        from argparse import Namespace
        
        print("\n" + "=" * 60)
        print("Generating All Reports".center(60))
        print("=" * 60)
        
        args = Namespace(date=options["date"], assets_dir=options["assets_dir"], output_dir=options["output_dir"])
        return generate_all(args)

    def run_flexible_module(self, options: Dict[str, Any]) -> int:
        """
        Run the flexible-module command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.reports.flexible_module import generate_flexible_module_report
        
        print("\n" + "=" * 60)
        print("Generating Flexible Module Report".center(60))
        print("=" * 60)
        
        return generate_flexible_module_report(
            options["date"],
            options.get("all_modules"),
            options.get("subset_modules"),
            options.get("exclude_modules"),
            options.get("output_prefix"),
            options.get("count_partial"),
            options.get("assets_dir"),
            options.get("output_dir")
        )

    def run_flexible_assessment(self, options: Dict[str, Any]) -> int:
        """
        Run the flexible-assessment command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.reports.flexible_assessment import generate_flexible_assessment_report
        
        print("\n" + "=" * 60)
        print("Generating Flexible Assessment Report".center(60))
        print("=" * 60)
        
        return generate_flexible_assessment_report(
            options["date"],
            options.get("assessment_types"),
            options.get("output_prefix"),
            options.get("assets_dir"),
            options.get("output_dir")
        )

    def run_flexible_grades(self, options: Dict[str, Any]) -> int:
        """
        Run the flexible-grades command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.reports.flexible_grades import generate_flexible_grades_report
        
        print("\n" + "=" * 60)
        print("Generating Flexible Grades Report".center(60))
        print("=" * 60)
        
        return generate_flexible_grades_report(
            options["date"],
            options.get("grade_categories"),
            options.get("grade_weights"),
            options.get("output_prefix"),
            options.get("assets_dir"),
            options.get("output_dir")
        )

    def run_markdown_to_pdf(self, options: Dict[str, Any]) -> int:
        """
        Run the markdown-to-pdf command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
        
        print("\n" + "=" * 60)
        print("Converting Markdown to PDF".center(60))
        print("=" * 60)
        
        return convert_markdown_to_pdf(
            options["input_dir"],
            options["output_dir"]
        )
        
    def run_student_reports(self, options: Dict[str, Any]) -> int:
        """
        Run the student reports command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.reports.report_generator import generate_student_reports
        
        print("\n" + "=" * 60)
        print("Generating Student Reports".center(60))
        print("=" * 60)
        
        # Ensure the output directory exists
        os.makedirs(options["output_dir"], exist_ok=True)
        
        return generate_student_reports(options["date"], options["output_dir"], options["assets_dir"])
        
    def run_class_summary(self, options: Dict[str, Any]) -> int:
        """
        Run the class summary command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        from compita.reports.report_generator import generate_class_summary
        
        print("\n" + "=" * 60)
        print("Generating Class Summary".center(60))
        print("=" * 60)
        
        # Ensure the output directory exists
        os.makedirs(options["output_dir"], exist_ok=True)
        
        return generate_class_summary(options["date"], options["output_dir"], options["assets_dir"])

    def run_csv_module_report(self, options: Dict[str, Any]) -> int:
        """
        Run the CSV module report command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        import sys
        from scripts.generate_reports import main as generate_reports_main
        
        print("\n" + "=" * 60)
        print("Generating CSV Module Report".center(60))
        print("=" * 60)
        
        # Prepare arguments for the generate_reports.py script
        sys.argv = ['generate_reports.py', 
                   '--date', options["date"],
                   '--module', str(options["module"]),
                   '--assets-dir', options["assets_dir"],
                   '--output-dir', options["output_dir"]]
        
        if "current_module" in options and options["current_module"]:
            sys.argv.extend(['--current-module', str(options["current_module"])])
        
        return generate_reports_main()

    def run_csv_student_report(self, options: Dict[str, Any]) -> int:
        """
        Run the CSV student report command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        import sys
        from scripts.generate_reports import main as generate_reports_main
        
        print("\n" + "=" * 60)
        print("Generating CSV Student Report".center(60))
        print("=" * 60)
        
        # Prepare arguments for the generate_reports.py script
        sys.argv = ['generate_reports.py', 
                   '--date', options["date"],
                   '--student', options["student"],
                   '--assets-dir', options["assets_dir"],
                   '--output-dir', options["output_dir"]]
        
        return generate_reports_main()

    def run_csv_class_report(self, options: Dict[str, Any]) -> int:
        """
        Run the CSV class report command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        import sys
        from scripts.generate_reports import main as generate_reports_main
        
        print("\n" + "=" * 60)
        print("Generating CSV Class Report".center(60))
        print("=" * 60)
        
        # Prepare arguments for the generate_reports.py script
        sys.argv = ['generate_reports.py', 
                   '--date', options["date"],
                   '--assets-dir', options["assets_dir"],
                   '--output-dir', options["output_dir"]]
        
        if "current_module" in options and options["current_module"]:
            sys.argv.extend(['--current-module', str(options["current_module"])])
        
        return generate_reports_main()

    def run_excel_report(self, options: Dict[str, Any]) -> int:
        """
        Run the Excel report command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        import sys
        from scripts.generate_reports import main as generate_reports_main
        
        print("\n" + "=" * 60)
        print("Generating Excel Report".center(60))
        print("=" * 60)
        
        # Prepare arguments for the generate_reports.py script
        sys.argv = ['generate_reports.py', 
                   '--date', options["date"],
                   '--excel',
                   '--assets-dir', options["assets_dir"],
                   '--output-dir', options["output_dir"]]
        
        if "current_module" in options and options["current_module"]:
            sys.argv.extend(['--current-module', str(options["current_module"])])
        
        return generate_reports_main()

    def run_all_csv_reports(self, options: Dict[str, Any]) -> int:
        """
        Run the all CSV reports command.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        import sys
        from scripts.generate_reports import main as generate_reports_main
        
        print("\n" + "=" * 60)
        print("Generating All CSV Reports".center(60))
        print("=" * 60)
        
        # Prepare arguments for the generate_reports.py script
        sys.argv = ['generate_reports.py', 
                   '--date', options["date"],
                   '--all',
                   '--assets-dir', options["assets_dir"],
                   '--output-dir', options["output_dir"]]
        
        if "current_module" in options and options["current_module"]:
            sys.argv.extend(['--current-module', str(options["current_module"])])
        
        return generate_reports_main()

    def quit(self, options: Dict[str, Any]) -> int:
        """
        Quit the application.
        
        Args:
            options: The options for the command
            
        Returns:
            The exit code
        """
        print("\nExiting Cyber8 Report Generator. Goodbye!")
        sys.exit(0)

    def run(self) -> int:
        """
        Run the interactive CLI.
        
        Returns:
            The exit code
        """
        while True:
            try:
                self.display_menu()
                choice = self.get_input("Enter your choice")
                
                if choice in self.commands:
                    command = self.commands[choice]
                    options = self.collect_options(command["options"])
                    
                    if self.confirm_run(command["name"], options):
                        try:
                            result = command["function"](options)
                            
                            if result == 0:
                                print("\n✅ Command completed successfully!")
                            else:
                                print(f"\n❌ Command failed with exit code: {result}")
                                
                            input("\nPress Enter to continue...")
                            return result
                        except Exception as e:
                            print(f"\n❌ Error running command: {e}")
                            input("\nPress Enter to continue...")
                            return 1
                elif choice.lower() in ['exit', 'quit', 'q']:
                    return self.quit({})
                else:
                    print(f"\n❌ Invalid choice: {choice}")
                    input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("\nPress Enter to continue...")


def main() -> int:
    """
    Run the interactive CLI.
    
    Returns:
        The exit code
    """
    try:
        cli = InteractiveCLI()
        return cli.run()
    except KeyboardInterrupt:
        print("\nExiting Cyber8 Report Generator. Goodbye!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

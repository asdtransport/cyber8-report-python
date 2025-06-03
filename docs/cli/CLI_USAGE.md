# CompITA Report Generator CLI

The CompITA Report Generator features an enhanced command-line interface with both traditional command-line arguments and an interactive mode. The CLI can be run from anywhere on your Mac.

## Running the CLI

You can run the CLI in two ways:

1. **From the project directory**:
   ```bash
   ./compita-cli [options]
   ```

2. **From anywhere on your Mac**:
   ```bash
   compita [options]
   ```

## Interactive CLI

The interactive CLI provides a user-friendly interface for generating various types of reports without having to remember all the command-line arguments.

### Running the Interactive CLI

To run the interactive CLI, use the `--interactive` or `-i` flag:

```bash
compita --interactive
```

### Features

The interactive CLI offers the following features:

1. **Menu-Based Navigation**: Select from a list of available report types
2. **Guided Option Configuration**: Step-by-step prompts for each required option
3. **Default Values**: Common options have sensible defaults
4. **Confirmation**: Review your selections before running the command
5. **Error Handling**: Graceful handling of errors and interruptions

### Available Commands

The interactive CLI supports the following commands:

1. **Generate All Reports**: Generate all reports for a specific date
2. **Flexible Module Report**: Generate flexible module report with customizable module selections
3. **Flexible Assessment Report**: Generate flexible assessment report with customizable assessment types
4. **Flexible Grades Report**: Generate flexible grades report with customizable grade categories and weights
5. **Markdown to PDF Conversion**: Convert markdown files to PDF
6. **Student Reports**: Generate individual student reports
7. **Class Summary**: Generate class summary report
8. **CSV Module Report**: Generate CSV report for a specific module
9. **CSV Student Report**: Generate CSV report for a specific student
10. **CSV Class Report**: Generate CSV report for the entire class
11. **Excel Report**: Generate Excel report with multiple sheets
12. **All CSV Reports**: Generate all CSV reports (modules, students, class, Excel)

## Traditional CLI

The traditional command-line interface is available for scripting and automation purposes.

### Available Commands

```bash
# Generate all reports
compita generate-all --date YY-MM-DD

# Generate flexible module report
compita flexible-module --date YY-MM-DD [--all-modules MOD1 MOD2...] [--subset-modules MOD1 MOD2...] [--exclude-modules MOD1 MOD2...] [--output-prefix PREFIX] [--count-partial]

# Generate flexible assessment report
compita flexible-assessment --date YY-MM-DD [--assessment-types TYPE1 TYPE2...] [--output-prefix PREFIX]

# Generate flexible grades report
compita flexible-grades --date YY-MM-DD [--grade-categories CAT1 CAT2...] [--grade-weights W1 W2...] [--output-prefix PREFIX]

# Convert markdown to PDF
compita markdown-to-pdf --input-dir INPUT_DIR --output-dir OUTPUT_DIR

# Generate CSV module report
compita csv-module --date YY-MM-DD --module MODULE_NUMBER [--current-module CURRENT_MODULE]

# Generate CSV student report
compita csv-student --date YY-MM-DD --student "STUDENT_NAME"

# Generate CSV class report
compita csv-class --date YY-MM-DD [--current-module CURRENT_MODULE]

# Generate Excel report
compita excel-report --date YY-MM-DD [--current-module CURRENT_MODULE]

# Generate all CSV reports
compita csv-all --date YY-MM-DD [--current-module CURRENT_MODULE]
```

## Examples

### Interactive Mode

```bash
# Run in interactive mode
compita --interactive
```

### Traditional Mode

```bash
# Generate all reports for May 5, 2025
compita generate-all --date 25-05-05

# Generate flexible module report for modules 1, 2, and 3
compita flexible-module --date 25-05-05 --all-modules 1 2 3 --output-prefix module_report

# Generate flexible assessment report for quizzes and exams
compita flexible-assessment --date 25-05-05 --assessment-types quiz exam --output-prefix assessment_report

# Generate flexible grades report with custom weights
compita flexible-grades --date 25-05-05 --grade-categories quiz exam project --grade-weights 0.3 0.4 0.3 --output-prefix grades_report

# Convert markdown to PDF
compita markdown-to-pdf --input-dir reports/25-05-05/progress_reports/student_reports --output-dir reports/25-05-05/executive_reports/student_reports

# Generate CSV module report for module 3
compita csv-module --date 25-05-05 --module 3 --current-module 7

# Generate CSV student report for John Smith
compita csv-student --date 25-05-05 --student "Smith, John"

# Generate CSV class report
compita csv-class --date 25-05-05 --current-module 7

# Generate Excel report with multiple sheets
compita excel-report --date 25-05-05 --current-module 7

# Generate all CSV reports
compita csv-all --date 25-05-05 --current-module 7
```

## Global Installation

The CompITA CLI has been set up to run from anywhere on your Mac. This was done by creating a symlink in your `~/bin` directory that points to the CLI script in the project directory. The `~/bin` directory has been added to your PATH in your `.zshrc` file.

For more details on the global installation, see the [GLOBAL_CLI_USAGE.md](GLOBAL_CLI_USAGE.md) file.

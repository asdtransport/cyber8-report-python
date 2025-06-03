# Markdown to PDF Converter

This tool converts the markdown progress reports into professionally formatted PDF files that resemble academic reports from prestigious institutions.

## Features

- **Professional Styling**: Elegant typography and layout inspired by Ivy League academic reports
- **Institutional Branding**: Customizable header with logo and institution name
- **Consistent Formatting**: Uniform styling across all reports
- **Watermarking**: Subtle "CONFIDENTIAL" watermark for document security
- **Page Numbering**: Automatic page numbers for multi-page reports
- **Responsive Tables**: Well-formatted tables for data presentation
- **PDF Bookmarks**: Automatic bookmarks based on report headings
- **Custom Templates**: Separate templates for student reports and class summaries

## Installation

The Markdown to PDF Converter requires the following dependencies:
- Python 3.8+
- markdown
- weasyprint
- jinja2

Install the dependencies:

```bash
source .venv/bin/activate
pip install markdown weasyprint jinja2
```

Note: WeasyPrint has some system dependencies. On macOS, you may need to install Cairo, Pango, and GDK-PixBuf using Homebrew:

```bash
brew install cairo pango gdk-pixbuf
```

## Usage

### Basic Usage

To convert a directory of markdown reports to PDFs:

```bash
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports --output-dir reports/25-05-05/pdf_reports
```

### Custom Logo

To use a custom logo in the reports:

```bash
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports --output-dir reports/25-05-05/pdf_reports --logo path/to/your/logo.png
```

### Custom Templates

You can customize the templates by modifying the HTML files in the `templates` directory:

- `base.html`: The base template with overall styling
- `student_report.html`: Template for individual student reports
- `class_summary.html`: Template for class summary reports

## Integration with Report Generator

You can easily integrate the PDF generation with the existing report generator:

```bash
# Generate reports and convert to PDF in one step
source .venv/bin/activate
python report_generator.py --date 25-05-05 --all --class-summary
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports --output-dir reports/25-05-05/pdf_reports
```

## Output

The PDF reports will be organized in the same structure as the markdown reports:

```
reports/
└── YY-MM-DD/
    └── pdf_reports/
        ├── student_reports/
        │   ├── Student1_report.pdf
        │   ├── Student2_report.pdf
        │   └── ...
        └── class_summaries/
            └── class_summary_report.pdf
```

## Customization

The PDF styling can be customized by editing the CSS in the `base.html` template. The current styling includes:

- Garamond font for an academic feel
- Crimson accent color (#8A0808) for headers and highlights
- Clean table formatting
- Highlighted recommendation sections
- Professional header with logo and institution name
- Confidential watermark
- Page numbering and date headers

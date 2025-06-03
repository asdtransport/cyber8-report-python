#!/usr/bin/env python3
"""
Markdown to PDF Converter

This script converts markdown reports to professionally formatted PDF files
that resemble academic progress reports from prestigious institutions.
"""

import os
import argparse
import markdown
import weasyprint
from datetime import datetime
import glob
import shutil
from jinja2 import Environment, FileSystemLoader


class MarkdownToPDF:
    """A class to convert markdown reports to professionally formatted PDFs."""

    def __init__(self, input_dir, output_dir, template_dir=None, logo_path=None):
        """
        Initialize the MarkdownToPDF converter.
        
        Args:
            input_dir (str): Directory containing markdown files
            output_dir (str): Directory to save PDF files
            template_dir (str, optional): Directory to store template files
            logo_path (str, optional): Path to logo image
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.template_dir = template_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.logo_path = logo_path
        
        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # Force regeneration of template files
        self._create_template_files(force=True)
        
        # Create assets directory and copy logo if provided
        self._setup_assets()

    def _create_template_files(self, force=False):
        """Create HTML template files if they don't exist."""
        # Base template
        base_template_path = os.path.join(self.template_dir, "base.html")
        if not os.path.exists(base_template_path) or force:
            with open(base_template_path, "w") as f:
                f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        @page {
            size: letter;
            margin: 1in;
            @top-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                font-family: 'Palatino', serif;
                color: #333;
            }
            @top-left {
                content: "Cyber 8";
                font-size: 10pt;
                font-family: 'Palatino', serif;
                color: #333;
            }
            @bottom-center {
                content: "CONFIDENTIAL - For Academic Use Only";
                font-size: 9pt;
                font-family: 'Palatino', serif;
                color: #666;
            }
        }
        body {
            font-family: 'Palatino', serif;
            line-height: 1.6;
            color: #333;
            margin: 0.4in 0.3in;
            padding: 0;
            font-size: 11pt;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 3px solid #00356B;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }
        .logo {
            height: 80px;
        }
        .header-text {
            text-align: right;
        }
        .header-text h1 {
            font-size: 28pt;
            margin: 0;
            color: #00356B;
            font-weight: normal;
        }
        .header-text p {
            font-size: 14pt;
            margin: 5px 0 0 0;
            color: #555;
        }
        .report-date {
            font-size: 12pt;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }
        h1, h2, h3, h4 {
            font-family: 'Palatino', serif;
            color: #00356B;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: normal;
        }
        h1 {
            font-size: 24pt;
            border-bottom: 1px solid #00356B;
            padding-bottom: 5px;
        }
        h2 {
            font-size: 20pt;
            border-bottom: 1px solid #ddd;
            padding-bottom: 3px;
        }
        h3 {
            font-size: 16pt;
        }
        h4 {
            font-size: 14pt;
            font-style: italic;
        }
        p {
            margin: 0.8em 0;
            text-align: justify;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 9pt;
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
            page-break-inside: avoid;
            table-layout: fixed;
            max-width: 100%;
            overflow-x: hidden;
        }
        thead {
            display: table-header-group;
            background-color: #00356B;
            color: white;
        }
        tbody {
            display: table-row-group;
        }
        th {
            background-color: #00356B;
            color: white;
            border: 1px solid #00356B;
            padding: 10px;
            text-align: left;
            font-weight: normal;
        }
        td {
            border: 1px solid #ddd;
            padding: 4px 6px;
            text-align: left;
            vertical-align: top;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .detailed-metrics-table {
            margin-top: 30px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }
        .detailed-metrics-table table {
            font-size: 10pt;
        }
        h3 + table {
            width: 100%;
            margin-top: 15px;
            margin-bottom: 30px;
        }
        h3 + table th:first-child {
            width: 40%;
        }
        h3 + table th:last-child {
            width: 60%;
        }
        h3[id="individual-module-details"] + table th:first-child {
            width: 15%;
        }
        h3[id="individual-module-details"] + table th:nth-child(2) {
            width: 20%;
        }
        h3[id="individual-module-details"] + table th:nth-child(3) {
            width: 20%;
        }
        h3[id="individual-module-details"] + table th:nth-child(4) {
            width: 20%;
        }
        h3[id="individual-module-details"] + table th:last-child {
            width: 25%;
        }
        .footer {
            margin-top: 50px;
            border-top: 2px solid #00356B;
            padding-top: 15px;
            font-size: 10pt;
            color: #666;
        }
        .footer-columns {
            display: flex;
            justify-content: space-between;
        }
        .footer-column {
            flex: 1;
            padding: 0 15px;
        }
        .footer-column:first-child {
            padding-left: 0;
        }
        .footer-column:last-child {
            padding-right: 0;
            text-align: right;
        }
        .recommendations {
            background-color: #f5f9ff;
            border-left: 4px solid #00356B;
            padding: 15px 20px;
            margin: 1.5em 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            page-break-inside: avoid;
        }
        .recommendations h2 {
            margin-top: 0;
            border-bottom: none;
            color: #00356B;
        }
        .recommendations ul {
            margin-bottom: 0;
        }
        .summary-box {
            background-color: #f5f9ff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 25px;
            margin: 1.5em 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            page-break-inside: avoid;
        }
        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 80pt;
            color: rgba(0, 53, 107, 0.03);
            z-index: -1;
        }
        .student-info {
            background-color: #f5f9ff;
            padding: 20px 25px;
            margin-bottom: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            page-break-inside: avoid;
        }
        .student-info h1 {
            color: #00356B;
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 26pt;
            border-bottom: none;
        }
        .student-details {
            display: flex;
            justify-content: space-between;
        }
        .student-info p {
            margin: 5px 0;
            font-size: 12pt;
        }
        .highlight {
            color: #00356B;
            font-weight: bold;
        }
        .progress-indicator {
            width: 100%;
            height: 10px;
            background-color: #eee;
            border-radius: 5px;
            margin: 5px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background-color: #00356B;
            border-radius: 5px;
        }
        .executive-summary {
            background-color: #f5f9ff;
            padding: 20px;
            margin: 20px 0 30px 0;
            border-left: 4px solid #00356B;
            font-size: 12pt;
            page-break-inside: avoid;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .executive-summary h2 {
            margin-top: 0;
            border-bottom: none;
            color: #00356B;
            font-size: 18pt;
        }
        .executive-summary p {
            margin: 10px 0;
            line-height: 1.5;
        }
        .data-highlight {
            font-size: 24pt;
            color: #00356B;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }
        .data-label {
            font-size: 11pt;
            color: #666;
            display: block;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }
        .metric-box {
            background-color: #f5f9ff;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border: 1px solid #e0e0e0;
        }
        ul li {
            margin-bottom: 8px;
        }
        /* Fix for table display issues */
        table, tr, td, th, tbody, thead, tfoot {
            page-break-inside: avoid !important;
        }
        table {
            display: table;
            width: 100%;
            border-collapse: collapse;
        }
        thead {
            display: table-header-group;
        }
        tbody {
            display: table-row-group;
        }
        tr {
            display: table-row;
        }
        td, th {
            display: table-cell;
        }
        
        /* Specific table styling */
        .summary-table {
            margin-top: 30px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
            width: 100%;
        }
        
        .summary-table th:first-child {
            width: 40%;
        }
        
        .summary-table th:last-child {
            width: 60%;
        }
        
        /* Module range tables */
        .module-range-table th:first-child {
            width: 40%;
        }
        
        .module-range-table th:last-child {
            width: 60%;
        }
        
        /* Module details table */
        .module-details-table {
            font-size: 10pt;
            width: 100%;
            table-layout: fixed;
        }
        
        .module-details-table th {
            padding: 8px;
            font-size: 10pt;
        }
        
        .module-details-table td {
            padding: 8px;
            font-size: 10pt;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        .module-details-table th:first-child {
            width: 10%;
        }
        
        .module-details-table th:nth-child(2) {
            width: 20%;
        }
        
        .module-details-table th:nth-child(3) {
            width: 20%;
        }
        
        .module-details-table th:nth-child(4) {
            width: 20%;
        }
        
        .module-details-table th:last-child {
            width: 30%;
        }
        
        /* Weekly activity table */
        .weekly-activity-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }
        
        .weekly-activity-table th {
            background-color: #00356B;
            color: white;
            padding: 8px 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .weekly-activity-table td {
            border-bottom: 1px solid #ddd;
            padding: 8px 10px;
            text-align: left;
        }
        
        .weekly-activity-table tr:nth-child(even) {
            background-color: #f5f9ff;
        }
        
        /* Make sure the week column is narrow */
        .weekly-activity-table td:first-child,
        .weekly-activity-table th:first-child {
            width: 60px;
            text-align: left;
        }
        
        /* Assessment table */
        .assessment-table th:first-child {
            width: 30%;
        }
        
        .data-table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            font-size: 11pt;
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
            page-break-inside: avoid;
            table-layout: fixed;
        }
        
        .data-table thead {
            display: table-header-group;
            background-color: #00356B;
            color: white;
        }
        
        .data-table tbody {
            display: table-row-group;
        }
        
        .data-table th {
            background-color: #00356B;
            color: white;
            border: 1px solid #00356B;
            padding: 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .data-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }
        
        .data-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Overall Score table */
        .overall-score-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 11pt;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            page-break-inside: avoid;
        }
        
        .overall-score-table th {
            background-color: #00356B;
            color: white;
            border: 1px solid #00356B;
            padding: 12px 15px;
            text-align: left;
            font-weight: normal;
        }
        
        .overall-score-table td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }
        
        .overall-score-table tr:nth-child(even) {
            background-color: #f5f9ff;
        }
        
        .overall-score-table th:first-child {
            width: 40%;
        }
        
        .overall-score-table th:last-child {
            width: 60%;
        }
        
        /* Specific table styling */
        .summary-table {
            margin-top: 30px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
            width: 100%;
        }
        
        .summary-table th:first-child {
            width: 40%;
        }
        
        .summary-table th:last-child {
            width: 60%;
        }
        
        /* Module range tables */
        .module-range-table th:first-child {
            width: 40%;
        }
        
        .module-range-table th:last-child {
            width: 60%;
        }
        
        /* Module details table */
        .module-details-table th:first-child {
            width: 15%;
        }
        
        .module-details-table th:nth-child(2) {
            width: 20%;
        }
        
        .module-details-table th:nth-child(3) {
            width: 20%;
        }
        
        .module-details-table th:nth-child(4) {
            width: 20%;
        }
        
        .module-details-table th:last-child {
            width: 25%;
        }
        
        /* Weekly activity table */
        .weekly-activity-table th:first-child {
            width: 15%;
        }
        
        .weekly-activity-table th:nth-child(2) {
            width: 25%;
        }
        
        .weekly-activity-table th:nth-child(3) {
            width: 15%;
        }
        
        .weekly-activity-table th:nth-child(4) {
            width: 20%;
        }
        
        .weekly-activity-table th:last-child {
            width: 25%;
        }
        
        /* Assessment table */
        .assessment-table th:first-child {
            width: 30%;
        }
        
        .data-table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            font-size: 11pt;
            box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
            page-break-inside: avoid;
            table-layout: fixed;
        }
        
        .data-table thead {
            display: table-header-group;
            background-color: #00356B;
            color: white;
        }
        
        .data-table tbody {
            display: table-row-group;
        }
        
        .data-table th {
            background-color: #00356B;
            color: white;
            border: 1px solid #00356B;
            padding: 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .data-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }
        
        .data-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Module details section */
        .module-details-section {
            page-break-inside: avoid;
            margin-bottom: 30px;
        }
        
        /* Make sure tables don't overflow the page */
        table {
            max-width: 100%;
            overflow-x: hidden;
        }
        
        /* Basic table - simple clean styling */
        .basic-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 11pt;
        }
        
        .basic-table th {
            background-color: #00356B;
            color: white;
            border: 1px solid #00356B;
            padding: 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .basic-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        
        .basic-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Student Rankings tables */
        .student-rankings-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 10pt;
            page-break-inside: avoid;
            table-layout: fixed;
        }
        
        .student-rankings-table th {
            background-color: #00356B;
            color: white;
            padding: 8px 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .student-rankings-table td {
            border-bottom: 1px solid #ddd;
            padding: 8px 10px;
            text-align: left;
        }
        
        .student-rankings-table tr:nth-child(even) {
            background-color: #f5f9ff;
        }
        
        /* Make sure the ranking column is narrow */
        .student-rankings-table td:first-child,
        .student-rankings-table th:first-child {
            width: 40px;
            text-align: center;
        }
        
        /* Make sure the student name column has enough space */
        .student-rankings-table td:nth-child(2),
        .student-rankings-table th:nth-child(2) {
            width: 25%;
        }
        
        /* Module Completion table */
        .module-completion-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }
        
        .module-completion-table th {
            background-color: #00356B;
            color: white;
            padding: 8px 10px;
            text-align: left;
            font-weight: normal;
        }
        
        .module-completion-table td {
            border-bottom: 1px solid #ddd;
            padding: 8px 10px;
            text-align: left;
        }
        
        .module-completion-table tr:nth-child(even) {
            background-color: #f5f9ff;
        }
        
        /* Student Rankings section */
        h2 + table.student-rankings-table {
            page-break-before: avoid;
            page-break-inside: avoid;
            margin-top: 10px;
        }
        
        /* Keep headings with their content */
        h2 {
            page-break-after: avoid;
            margin-bottom: 10px;
        }
        
        /* Reduce space between sections */
        .content-wrapper h2 {
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        /* Ensure tables don't break across pages */
        table {
            page-break-inside: avoid;
        }
        
        /* Student Rankings section - keep everything together */
        .rankings-section, .module-section {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            display: block;
            margin-bottom: 20px;
        }
        
        /* Make the student rankings table more compact */
        .student-rankings-table {
            font-size: 9pt !important;
            line-height: 1.2 !important;
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            margin-top: 5px !important;
        }
        
        .student-rankings-table td,
        .student-rankings-table th {
            padding: 3px 5px !important;
        }
        
        /* Module completion table styling */
        .module-completion-table {
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            margin-top: 5px !important;
        }
        
        /* Reduce overall margins to fit more content */
        body {
            margin: 0.4in 0.3in;
        }
        
        /* Make all tables more compact */
        table {
            font-size: 9pt;
            margin-top: 5px !important;
            margin-bottom: 10px !important;
        }
        
        td, th {
            padding: 3px 5px;
        }
        
        /* Ensure headings stay with their content */
        h2 {
            page-break-before: auto;
            page-break-after: avoid !important;
            margin-bottom: 5px;
        }
        
        /* Force Student Rankings to stay together */
        h2:nth-of-type(2) {  /* Student Rankings is typically the 2nd h2 */
            page-break-before: auto !important;
            page-break-after: avoid !important;
            margin-bottom: 5px !important;
        }
        
        h2:nth-of-type(2) + table {
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            font-size: 9pt !important;
            line-height: 1.2 !important;
        }
        
        h2:nth-of-type(2) + table td,
        h2:nth-of-type(2) + table th {
            padding: 3px 5px !important;
        }
        
        /* Force Module Completion to stay together */
        h2:nth-of-type(3) {  /* Module Completion is typically the 3rd h2 */
            page-break-before: auto !important;
            page-break-after: avoid !important;
            margin-bottom: 5px !important;
        }
        
        h2:nth-of-type(3) + table {
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            font-size: 9pt !important;
            line-height: 1.2 !important;
        }
        
        h2:nth-of-type(3) + table td,
        h2:nth-of-type(3) + table th {
            padding: 3px 5px !important;
        }
        
        /* Force Weekly Activity to stay together */
        h2:nth-of-type(4) {  /* Weekly Activity is typically the 4th h2 */
            page-break-before: auto !important;
            page-break-after: avoid !important;
            margin-bottom: 5px !important;
        }
        
        h2:nth-of-type(4) + table {
            page-break-before: avoid !important;
            page-break-inside: avoid !important;
            font-size: 9pt !important;
            line-height: 1.2 !important;
        }
        
        h2:nth-of-type(4) + table td,
        h2:nth-of-type(4) + table th {
            padding: 3px 5px !important;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            {% if logo_path %}
            <img src="{{ logo_path }}" alt="Logo" class="logo">
            {% endif %}
        </div>
        <div class="header-text">
            <h1>Cyber 8 Cohort</h1>
            <p>Excellence in Technical Education</p>
            <p class="report-date">{{ report_date }}</p>
        </div>
    </div>
    
    <div class="watermark">CONFIDENTIAL</div>
    
    {{ content|safe }}
    
    <div class="footer">
        <div class="footer-columns">
            <div class="footer-column">
                <p><strong>City of Refuge</strong><br>
                1300 Joseph E. Boone Blvd NW<br>
                Atlanta, GA 30314</p>
            </div>
            <div class="footer-column">
                <p>Report generated on:<br>
                {{ report_date }}</p>
            </div>
            <div class="footer-column">
                <p>Cyber8 Report Generator</p>
            </div>
        </div>
        <p style="text-align: center; margin-top: 15px;">This report is confidential and intended for the student and authorized academic personnel only.</p>
        <p style="text-align: center; margin-top: 15px;">Copyright 2025 Cyber8. All rights reserved.</p>
    </div>
</body>
</html>""")
        
        # Student report template
        student_template_path = os.path.join(self.template_dir, "student_report.html")
        if not os.path.exists(student_template_path) or force:
            with open(student_template_path, "w") as f:
                f.write("""{% extends "base.html" %}

{% block content %}
    {{ content|safe }}
{% endblock %}""")
        
        # Class summary template
        class_template_path = os.path.join(self.template_dir, "class_summary.html")
        if not os.path.exists(class_template_path) or force:
            with open(class_template_path, "w") as f:
                f.write("""{% extends "base.html" %}

{% block content %}
    {{ content|safe }}
{% endblock %}""")

    def _setup_assets(self):
        """Set up assets directory and copy logo if provided."""
        assets_dir = os.path.join(self.template_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        
        # Create a default logo if none is provided
        if not self.logo_path:
            self.logo_path = os.path.join(assets_dir, "default_logo.png")
            # If default logo doesn't exist, create a placeholder
            if not os.path.exists(self.logo_path):
                # Create a simple placeholder logo
                try:
                    from PIL import Image, ImageDraw
                    
                    # Create a blank image with a white background
                    img = Image.new('RGB', (200, 60), color=(255, 255, 255))
                    d = ImageDraw.Draw(img)
                    
                    # Draw a blue rectangle as a simple logo
                    d.rectangle([(10, 10), (190, 50)], fill=(0, 53, 107))
                    
                    # Save the image
                    img.save(self.logo_path)
                    print(f"Created placeholder logo at {self.logo_path}")
                except ImportError:
                    print("PIL not available, skipping logo creation")
                    # Just create an empty file to prevent future errors
                    with open(self.logo_path, 'wb') as f:
                        f.write(b'')
        else:
            # Copy the provided logo to assets directory
            logo_filename = os.path.basename(self.logo_path)
            logo_destination = os.path.join(assets_dir, logo_filename)
            if not os.path.exists(logo_destination):
                shutil.copy(self.logo_path, logo_destination)
            self.logo_path = logo_destination

    def convert_markdown_to_html(self, markdown_content, is_class_summary=False):
        """
        Convert markdown content to HTML.
        
        Args:
            markdown_content (str): Markdown content to convert
            is_class_summary (bool): Whether this is a class summary report
            
        Returns:
            str: HTML content
        """
        # Extract student information before conversion
        student_info = self._extract_student_info(markdown_content)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc'
            ]
        )
        
        # Add student info section at the top if it's a student report
        if student_info and 'name' in student_info and not is_class_summary:
            html_content = self._add_student_info_section(html_content, student_info)
        
        # Apply basic styling to tables
        html_content = self._enhance_tables(html_content, is_class_summary=is_class_summary)
        
        return html_content
    
    def _extract_student_info(self, markdown_content):
        """
        Extract student information from markdown content.
        
        Args:
            markdown_content (str): Markdown content
            
        Returns:
            dict: Student information
        """
        import re
        
        student_info = {}
        
        # Extract student name
        name_match = re.search(r'# Progress Report: (.*?)$', markdown_content, re.MULTILINE)
        if name_match:
            student_info['name'] = name_match.group(1).strip()
        
        # Extract email
        email_match = re.search(r'\*\*Email:\*\* (.*?)$', markdown_content, re.MULTILINE)
        if email_match:
            student_info['email'] = email_match.group(1).strip()
        
        # Extract report date
        date_match = re.search(r'\*\*Report Date:\*\* (.*?)$', markdown_content, re.MULTILINE)
        if date_match:
            student_info['report_date'] = date_match.group(1).strip()
        
        return student_info
    
    def _add_student_info_section(self, html_content, student_info):
        """
        Add student information section to HTML content.
        
        Args:
            html_content (str): HTML content
            student_info (dict): Student information
            
        Returns:
            str: HTML content with student info section
        """
        student_section = '<div class="student-info">'
        
        if 'name' in student_info:
            # Add student name as a heading
            student_section += f'<h1 class="student-name">{student_info["name"]}</h1>'
            
            # Remove the original h1 title to avoid duplication
            html_content = html_content.replace(f'<h1>Progress Report: {student_info["name"]}</h1>', '')
        
        student_section += '<div class="student-details">'
        
        if 'email' in student_info:
            student_section += f'<p><strong>Email:</strong> {student_info["email"]}</p>'
        
        if 'report_date' in student_info:
            student_section += f'<p><strong>Report Date:</strong> {student_info["report_date"]}</p>'
        
        student_section += '</div></div>'
        
        # Add the student section at the beginning of the content
        html_content = student_section + html_content
        
        return html_content

    def _enhance_tables(self, html_content, is_class_summary=False):
        """
        Enhance tables with basic styling.
        
        Args:
            html_content (str): HTML content to enhance
            is_class_summary (bool): Whether this is a class summary report
            
        Returns:
            str: Enhanced HTML content
        """
        import re
        
        # Add classes to tables for styling
        html_content = re.sub(r'<table>', '<table class="data-table">', html_content)
        
        # Add executive summary section after the header - only for student reports
        if '<h2>Summary</h2>' in html_content and not is_class_summary:
            # Extract student name if available
            student_name = ""
            name_match = re.search(r'<h1 class="student-name">(.*?)</h1>', html_content)
            if name_match:
                student_name = name_match.group(1)
                
            # Create personalized executive summary
            if student_name:
                executive_summary = f'''
                <div class="executive-summary">
                    <h2>Executive Summary</h2>
                    <p>This report provides a comprehensive analysis of {student_name}'s academic performance and engagement metrics.
                    It highlights key achievements, areas of strength, and opportunities for improvement.</p>
                    <p>The data presented in this report is based on continuous assessment and monitoring of learning activities,
                    including module completion, assessment scores, and study time allocation.</p>
                </div>
                '''
                
                # Insert the executive summary after the student info section but before the first h2
                first_h2_pos = html_content.find('<h2>')
                if first_h2_pos > 0:
                    html_content = html_content[:first_h2_pos] + executive_summary + html_content[first_h2_pos:]
        
        # Add metrics grid after the Summary section - only for student reports
        if '<h2>Summary</h2>' in html_content and not is_class_summary:
            # Extract key metrics from the HTML content
            completion_match = re.search(r'Overall Completion: (\d+\.?\d*%)', html_content)
            completion = completion_match.group(1) if completion_match else "N/A"
            
            study_time_match = re.search(r'Total Study Time: (\d+\.?\d*) hours', html_content)
            study_time = study_time_match.group(1) if study_time_match else "N/A"
            
            assessments_match = re.search(r'Assessments Completed: (\d+)', html_content)
            assessments = assessments_match.group(1) if assessments_match else "N/A"
            
            # Create metrics grid
            metrics_grid = f'''
            <div class="metrics-grid">
                <div class="metric-box">
                    <span class="data-highlight">{completion}</span>
                    <span class="data-label">Overall Completion</span>
                </div>
                <div class="metric-box">
                    <span class="data-highlight">{study_time}</span>
                    <span class="data-label">Total Study Hours</span>
                </div>
                <div class="metric-box">
                    <span class="data-highlight">{assessments}</span>
                    <span class="data-label">Assessments Completed</span>
                </div>
            </div>
            '''
            
            # Insert metrics grid after the Summary section
            summary_end_pos = html_content.find('</p>', html_content.find('<h2>Summary</h2>'))
            if summary_end_pos > 0:
                html_content = html_content[:summary_end_pos + 4] + metrics_grid + html_content[summary_end_pos + 4:]
        
        # Add thead to tables that don't have it
        table_pattern = r'<table class="data-table">(.*?)<tr>(.*?)</tr>'
        
        def add_thead(match):
            table_start = match.group(1)
            first_row = match.group(2)
            
            # Check if this is a header row (contains th)
            if '<th>' in first_row:
                return f'<table class="data-table"><thead><tr>{first_row}</tr></thead>{table_start}'
            else:
                # Create header row from the first row
                header_row = first_row.replace('<td>', '<th>').replace('</td>', '</th>')
                return f'<table class="data-table"><thead><tr>{header_row}</tr></thead>{table_start}<tr>{first_row}</tr>'
        
        html_content = re.sub(table_pattern, add_thead, html_content, flags=re.DOTALL)
        
        # Special handling for Student Rankings section in class summary
        if is_class_summary and '<h2>Student Rankings</h2>' in html_content:
            # Find the heading and add an id
            rankings_start = html_content.find('<h2>Student Rankings</h2>')
            h2_end = html_content.find('</h2>', rankings_start)
            if h2_end > 0:
                html_content = html_content[:h2_end] + ' id="student-rankings-heading"' + html_content[h2_end:]
            
            # Find the table that follows the Student Rankings heading
            table_start = html_content.find('<table class="data-table">', rankings_start)
            if table_start > 0:
                # Add a specific class to the table for targeted styling
                html_content = html_content[:table_start] + '<table class="data-table student-rankings-table">' + html_content[table_start + len('<table class="data-table">'):]
                
                # Wrap the entire section in a div to keep it together
                section_end = html_content.find('<h2>', rankings_start + 1)
                if section_end == -1:  # If it's the last section
                    section_end = html_content.find('</body>', rankings_start)
                if section_end > 0:
                    # Insert opening div before the heading
                    html_content = html_content[:rankings_start] + '<div class="rankings-section">' + html_content[rankings_start:section_end] + '</div>' + html_content[section_end:]
        
        # Special handling for Module Completion section in class summary
        if is_class_summary and '<h2>Module Completion</h2>' in html_content:
            completion_start = html_content.find('<h2>Module Completion</h2>')
            table_start = html_content.find('<table class="data-table">', completion_start)
            if table_start > 0:
                html_content = html_content[:table_start] + '<table class="data-table module-completion-table">' + html_content[table_start + len('<table class="data-table">'):]
                
                # Wrap the entire section in a div to keep it together
                section_end = html_content.find('<h2>', completion_start + 1)
                if section_end == -1:  # If it's the last section
                    section_end = html_content.find('</body>', completion_start)
                if section_end > 0:
                    # Insert opening div before the heading
                    html_content = html_content[:completion_start] + '<div class="module-section">' + html_content[completion_start:section_end] + '</div>' + html_content[section_end:]
        
        # Special handling for Overall Score section in class summary
        if '<h3>Overall Score</h3>' in html_content:
            overall_score_start = html_content.find('<h3>Overall Score</h3>')
            overall_score_end = html_content.find('<h3', overall_score_start + 1)
            if overall_score_end == -1:  # If it's the last section
                overall_score_end = html_content.find('</body>', overall_score_start)
            
            # Extract the Overall Score section
            overall_score_section = html_content[overall_score_start:overall_score_end]
            
            # Check if it contains a table
            if '<table' in overall_score_section:
                # Add special class to the table
                enhanced_section = overall_score_section.replace('<table class="data-table">', '<table class="student-rankings-table">')
                
                # Replace the section with the enhanced version
                html_content = html_content[:overall_score_start] + enhanced_section + html_content[overall_score_end:]
        
        # Special handling for Weekly Activity section
        if '<h2>Weekly Activity</h2>' in html_content:
            weekly_start = html_content.find('<h2>Weekly Activity</h2>')
            weekly_end = html_content.find('<h2', weekly_start + 1)
            if weekly_end == -1:  # If it's the last section
                weekly_end = html_content.find('</body>', weekly_start)
            
            # Extract the section
            weekly_section = html_content[weekly_start:weekly_end]
            
            # Check if it contains a table
            if '<table' in weekly_section:
                # Add special class to the table
                enhanced_section = weekly_section.replace('<table class="data-table">', '<table class="weekly-activity-table">')
                
                # Replace the section with the enhanced version
                html_content = html_content[:weekly_start] + enhanced_section + html_content[weekly_end:]
        
        # Add section-specific styling
        def add_section_specific_styling(html_content):
            # Add classes to different sections based on their headings
            
            # Summary section
            if '<h2>Summary</h2>' in html_content:
                summary_start = html_content.find('<h2>Summary</h2>')
                table_start = html_content.find('<table class="data-table">', summary_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table summary-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Module Range section
            if '<h3>Module Range</h3>' in html_content:
                module_range_start = html_content.find('<h3>Module Range</h3>')
                table_start = html_content.find('<table class="data-table">', module_range_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table module-range-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Assessment section
            if '<h3>Assessment</h3>' in html_content:
                assessment_start = html_content.find('<h3>Assessment</h3>')
                table_start = html_content.find('<table class="data-table">', assessment_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table assessment-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Weekly Activity section
            if '<h3>Weekly Activity</h3>' in html_content:
                weekly_start = html_content.find('<h3>Weekly Activity</h3>')
                table_start = html_content.find('<table class="data-table">', weekly_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table weekly-activity-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Module Progress section
            if '<h2>Module Progress</h2>' in html_content:
                module_progress_start = html_content.find('<h2>Module Progress</h2>')
                table_start = html_content.find('<table class="data-table">', module_progress_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table module-progress-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Student Rankings section for class summary
            if is_class_summary and '<h2>Student Rankings</h2>' in html_content:
                rankings_start = html_content.find('<h2>Student Rankings</h2>')
                table_start = html_content.find('<table class="data-table">', rankings_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table student-rankings-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            # Module Completion section for class summary
            if is_class_summary and '<h2>Module Completion</h2>' in html_content:
                completion_start = html_content.find('<h2>Module Completion</h2>')
                table_start = html_content.find('<table class="data-table">', completion_start)
                if table_start > 0:
                    html_content = html_content[:table_start] + '<table class="data-table module-completion-table">' + html_content[table_start + len('<table class="data-table">'):]
            
            return html_content
        
        # Apply section-specific styling
        html_content = add_section_specific_styling(html_content)
        
        # Enhance the recommendations section
        if '<h2>Recommendations</h2>' in html_content:
            html_content = html_content.replace('<h2>Recommendations</h2>', '<div class="recommendations"><h2>Recommendations</h2>')
            
            # If recommendations is followed by another h2
            if '</ul>\n<h2>' in html_content:
                html_content = html_content.replace('</ul>\n<h2>', '</ul></div>\n<h2>')
            # If recommendations is the last section
            elif '</ul>\n</body>' in html_content:
                html_content = html_content.replace('</ul>\n</body>', '</ul></div>\n</body>')
        
        return html_content

    def extract_title_from_markdown(self, markdown_content):
        """
        Extract title from markdown content.
        
        Args:
            markdown_content (str): Markdown content
            
        Returns:
            str: Title
        """
        lines = markdown_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Progress Report"

    def convert_file(self, markdown_file, is_class_summary=False):
        """
        Convert a markdown file to PDF.
        
        Args:
            markdown_file (str): Path to markdown file
            is_class_summary (bool): Whether this is a class summary report
            
        Returns:
            str: Path to output PDF file
        """
        # Determine output file path
        filename = os.path.basename(markdown_file)
        output_filename = os.path.splitext(filename)[0] + ".pdf"
        output_file = os.path.join(self.output_dir, output_filename)
        
        # Read markdown content
        with open(markdown_file, 'r') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML
        html_content = self.convert_markdown_to_html(markdown_content, is_class_summary=is_class_summary)
        
        # Get the title from the markdown content
        title = self.extract_title_from_markdown(markdown_content)
        
        # Get the report date
        report_date = self.extract_date_from_markdown(markdown_content) or datetime.now().strftime("%B %d, %Y")
        
        # Determine if this is a student report or class summary
        is_student_report = "Progress Report:" in markdown_content
        
        # Render the appropriate template
        if is_student_report:
            template = self.env.get_template("student_report.html")
        else:
            template = self.env.get_template("class_summary.html")
        
        # Render the template with the HTML content
        rendered_html = template.render(
            title=title,
            content=html_content,
            logo_path=self.logo_path,
            report_date=report_date
        )
        
        # Save the rendered HTML to a temporary file
        temp_html_file = os.path.join(self.output_dir, f"{os.path.basename(output_file)}.html")
        with open(temp_html_file, 'w') as f:
            f.write(rendered_html)
        
        # Convert HTML to PDF
        weasyprint.HTML(temp_html_file).write_pdf(output_file)
        
        # Remove temporary HTML file
        os.remove(temp_html_file)
        
        return output_file

    def extract_date_from_markdown(self, markdown_content):
        """
        Extract date from markdown content.
        
        Args:
            markdown_content (str): Markdown content
            
        Returns:
            str: Date
        """
        import re
        
        date_match = re.search(r'\*\*Report Date:\*\* (.*?)$', markdown_content, re.MULTILINE)
        if date_match:
            return date_match.group(1).strip()
        return None

    def convert_directory(self):
        """
        Convert all markdown files in the input directory to PDFs.
        
        Returns:
            list: Paths to generated PDF files
        """
        pdf_paths = []
        
        # Process student reports
        student_reports_dir = os.path.join(self.input_dir, "student_reports")
        if os.path.exists(student_reports_dir):
            for markdown_file in glob.glob(os.path.join(student_reports_dir, "*.md")):
                pdf_path = self.convert_file(markdown_file, is_class_summary=False)
                pdf_paths.append(pdf_path)
                print(f"Converted student report: {pdf_path}")
        
        # Process class summaries
        class_summaries_dir = os.path.join(self.input_dir, "class_summaries")
        if os.path.exists(class_summaries_dir):
            for markdown_file in glob.glob(os.path.join(class_summaries_dir, "*.md")):
                pdf_path = self.convert_file(markdown_file, is_class_summary=True)
                pdf_paths.append(pdf_path)
                print(f"Converted class summary: {pdf_path}")
        
        # Process any markdown files directly in the input directory
        for markdown_file in glob.glob(os.path.join(self.input_dir, "*.md")):
            # Determine if it's a class summary based on filename
            is_class_summary = "class_summary" in os.path.basename(markdown_file)
            pdf_path = self.convert_file(markdown_file, is_class_summary=is_class_summary)
            pdf_paths.append(pdf_path)
            print(f"Converted report: {pdf_path}")
        
        return pdf_paths


def main():
    """
    Main function to parse command line arguments and execute the converter.
    """
    parser = argparse.ArgumentParser(description='Convert markdown reports to PDF')
    parser.add_argument('--input-dir', required=True, help='Directory containing markdown files')
    parser.add_argument('--output-dir', required=True, help='Directory to save PDF files')
    parser.add_argument('--logo', help='Path to logo image file')
    args = parser.parse_args()
    
    # Create converter
    converter = MarkdownToPDF(args.input_dir, args.output_dir, logo_path=args.logo)
    
    # Find all markdown files in the input directory
    markdown_files = []
    for root, _, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    # Convert all markdown files to PDF
    pdf_files = []
    for markdown_file in markdown_files:
        # Check if this is a class summary report
        is_class_summary = 'class_summary' in os.path.basename(markdown_file).lower()
        
        # Convert the file
        pdf_file = converter.convert_file(markdown_file, is_class_summary=is_class_summary)
        
        # Determine the type of report for display purposes
        if is_class_summary:
            print(f"Converted class summary: {pdf_file}")
        else:
            print(f"Converted student report: {pdf_file}")
        
        pdf_files.append(pdf_file)
    
    # Print summary
    print(f"\nPDF generation complete! Generated {len(pdf_files)} PDF reports:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file}")


if __name__ == "__main__":
    main()

# Add adapter function for the new CLI interface
def convert_markdown_to_pdf(input_dir, output_dir, template_dir=None, logo_path=None):
    """
    Convert markdown files to PDF.
    
    Args:
        input_dir (str): Directory containing markdown files
        output_dir (str): Directory to save PDF files
        template_dir (str, optional): Directory to store template files
        logo_path (str, optional): Path to logo image
        
    Returns:
        list: Paths to the generated PDF files
    """
    converter = MarkdownToPDF(input_dir, output_dir, template_dir, logo_path)
    return converter.convert_directory()

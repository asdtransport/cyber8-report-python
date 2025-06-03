from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Ensure the assets directory is included
package_data = {
    "compita": [
        "templates/*",
        "templates/assets/*",
        "converters/templates/*",
        "converters/templates/assets/*",
        "src/web/*",
    ]
}

# Create a data_files list to include the assets directory
data_files = []
for root, dirs, files in os.walk("assets"):
    if files:
        data_files.append((root, [os.path.join(root, f) for f in files]))

setup(
    name="compita-report-generator",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data=package_data,
    data_files=data_files,
    install_requires=[
        "markdown",
        "weasyprint",
        "jinja2",
        "pandas",
        "numpy",
        "openpyxl",
        "flask",
    ],
    extras_require={
        "api": [
            "fastapi>=0.95.0",
            "uvicorn>=0.21.0",
            "python-multipart>=0.0.6",
            "pydantic>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "compita=compita.cli.main:main",
        ],
    },
    author="CompITA Team",
    author_email="info@compita.edu",
    description="A package for generating student progress reports from CompITA data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="education, reports, pdf, markdown",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Office/Business",
    ],
)

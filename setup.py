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
    name="cyber8-report-generator",
    version="1.0.0",
    packages=find_packages(include=['compita', 'compita.*']),
    include_package_data=True,
    package_data=package_data,
    zip_safe=False,
    data_files=data_files,
    install_requires=[
        "markdown",
        "weasyprint",
        "jinja2",
        "pandas",
        "numpy",
        "openpyxl",
        "flask",
        "python-dotenv",
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
            "cyber8=compita.cli.main:main",
        ],
    },
    author="Cyber8 Team",
    author_email="info@cyber8.org",
    description="A Python package for generating student progress reports from Cyber8 data",
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

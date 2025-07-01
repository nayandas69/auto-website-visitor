#!/usr/bin/env python3
"""Setup script for auto-website-visitor package."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="auto-website-visitor",
    version="1.0.0",
    author="nayandas69",
    author_email="nayanchandradas@hotmail.com",
    description="Automated website visitor with scheduling and advanced browser automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/auto-website-visitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.10",
    install_requires=[
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
        "schedule>=1.2.0",
        "croniter>=1.4.0",
        "colorama>=0.4.6",
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "packaging>=23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "awv=auto_website_visitor.cli:main",
            "auto-website-visitor=auto_website_visitor.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "auto_website_visitor": ["templates/*.yaml", "templates/*.json"],
    },
)
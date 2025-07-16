#!/usr/bin/env python3

"""Setup script for Auto Website Visitor."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="auto-website-visitor",
    version="3.0.0",
    author="nayandas69",
    author_email="nayanchandradas@hotmail.com",
    description="Automated website visitor with scheduling and advanced browser automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/auto-website-visitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    install_requires=requirements,
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
    zip_safe=False,
)

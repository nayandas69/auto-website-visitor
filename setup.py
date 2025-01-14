from setuptools import setup, find_packages

# Read the README.md for a long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-website-visitor",
    version="0.0.2",
    author="Nayan Das",
    author_email="nayanchandradas@hotmail.com",
    author_website="https://nayanchandradas.com",
    description=("A CLI tool to automate website visits using Selenium and Python."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/auto-website-visitor",
    project_urls={
        "Bug Tracker": "https://github.com/nayandas69/auto-website-visitor/issues",
        "Documentation": "https://github.com/nayandas69/auto-website-visitor#readme",
        "Source Code": "https://github.com/nayandas69/auto-website-visitor",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "auto website visitor", "website visitor", "automation", "selenium",
        "selenium python", "cli tool", "website traffic", "website automation",
    ],
    packages=find_packages(include=["*"], exclude=["tests*", "docs*"]),  # Automatically finds packages in the root
    py_modules=["main"],             # Single file module
    python_requires=">=3.6",         # Python version requirement
    install_requires=[
        "selenium>=4.0.0",
        "colorama>=0.4.4",
        "webdriver-manager>=3.8.0",
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "auto-website-visitor=main:main",  # Command to run the script
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)
# The setup() function is the core of the setup.py script. It takes a lot of arguments, but most of them are optional.
# Here's a breakdown of the arguments used in this script:
# name: The name of the package. This is what users will use to install the package using pip.
# version: The version of the package. This is used by pip to check for updates and dependencies.
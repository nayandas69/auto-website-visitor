from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto_website_visitor",
    version="0.0.7",
    author="nayandas69",
    author_email="nayanchandradas@hotmail.com",
    description=("A CLI tool to automate website traffic using Selenium."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/auto-website-visitor",
    project_urls={
        "Bug Tracker": "https://github.com/nayandas69/auto-website-visitor/issues",
        "Documentation": "https://github.com/nayandas69/auto-website-visitor#readme",
        "Source Code": "https://github.com/nayandas69/auto-website-visitor",
        "Discord Community": "https://discord.gg/skHyssu",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "auto website visitor",
        "website visitor",
        "automation",
        "selenium",
        "selenium python",
        "cli tool",
        "website traffic",
        "website automation",
        "auto visits",
        "traffic generator",
        "auto bot",
    ],
    packages=find_packages(
        include=["auto_website_visitor*"], exclude=["tests*", "docs*"]
    ),
    py_modules=["awv"],
    python_requires=">=3.7",
    install_requires=[
        "selenium>=4.10.0",
        "colorama>=0.4.4",
        "webdriver-manager>=3.8.0",
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "auto-website-visitor=awv:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)

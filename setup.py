from setuptools import setup, find_packages

# Yo fam, this script sets up the 🔥 "Auto Website Visitor" project.
# It’s like the VIP pass to package this tool and make it pip-ready. 🚀

# Reading README.md for the long description cuz we love giving all the deets. 📝
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-website-visitor",
    version="0.0.5",
    author="Nayan Das",  # Shoutout to the legend who made this. 🙌
    author_email="nayanchandradas@hotmail.com",  # Slide into my inbox (for legit stuff, obvi). 📧
    description=("A CLI tool to automate website traffic using Selenium. ☠️"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/auto-website-visitor",  # HQ of this awesome project. 🌐
    project_urls={  # Extra sauce: linking the docs, bugs, and source.
        "Bug Tracker": "https://github.com/nayandas69/auto-website-visitor/issues",
        "Documentation": "https://github.com/nayandas69/auto-website-visitor#readme",
        "Source Code": "https://github.com/nayandas69/auto-website-visitor",
    },
    classifiers=[  # Just flexing some official labels for PyPI. 💻
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[  # Some spicy tags so people can find this masterpiece. 🌶️
        "auto website visitor", "website visitor", "automation", "selenium",
        "selenium python", "cli tool", "website traffic", "website automation",
        "auto visits", "traffic generator", "auto bot"
    ],
    packages=find_packages(include=["auto_website_visitor*"], exclude=["tests*", "docs*"]),  # Includes expanded package paths. 🎒
    py_modules=["awv"],  # Branding matters. 💎
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.0.0",
        "colorama>=0.4.4",
        "webdriver-manager>=3.8.0",
        "requests>=2.25.1",
    ],
    entry_points={  # CLI magic happens here. 🪄
        "console_scripts": [
            "auto-website-visitor=awv:main",  # Command to run the tool straight from the terminal. 🔥
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)

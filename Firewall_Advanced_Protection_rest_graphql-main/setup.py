#!/usr/bin/env python3
"""
API Firewall - Enterprise Setup Script
Installs the firewall as a Python package for easy integration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="api-firewall-advanced",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Advanced API Firewall for REST and GraphQL APIs",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/api-firewall-advanced",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
            "plotly>=5.15.0",
            "pandas>=2.0.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "joblib>=1.3.0",
            "numpy>=1.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "api-firewall=backend.main:main",
            "firewall-dashboard=dashboard:main",
            "firewall-test=test_firewall:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json", "*.env"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/api-firewall-advanced/issues",
        "Source": "https://github.com/yourusername/api-firewall-advanced",
        "Documentation": "https://api-firewall-docs.readthedocs.io/",
    },
)
#!/usr/bin/env python3
"""
Setup script for AICommandExplainerAgent
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AICommandExplainerAgent - Smart Terminal Command Interpreter"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="ai-command-explainer-agent",
    version="1.0.0",
    description="AI-powered CLI agent that explains terminal/shell commands in plain English",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="100DaysOfAI-Agents",
    author_email="",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-command-explainer=main:main",
            "command-explainer=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai, cli, terminal, commands, explanation, shell, bash, powershell, education, development",
    project_urls={
        "Bug Reports": "",
        "Source": "",
        "Documentation": "",
    },
)

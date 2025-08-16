#!/usr/bin/env python3
"""
Setup script for WhatsApp Scheduler Agent
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="whatsapp-scheduler-agent",
    version="1.0.0",
    author="100 Days Agent Challenge",
    author_email="",
    description="A CLI-based WhatsApp message scheduler using WhatsApp Web",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "whatsapp-scheduler=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="whatsapp scheduler automation cli",
    project_urls={
        "Bug Reports": "",
        "Source": "",
        "Documentation": "",
    },
)

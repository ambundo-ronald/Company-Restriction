from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="company_restriction",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="Restrict users to specific companies in ERPNext with complete data isolation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ambundo-ronald/Company-Restriction",
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "frappe",
    ],
)

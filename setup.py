"""
MedLink - Unified Medical Records System
Setup configuration for package installation

Author: Youssef
Institution: Elsewedy University of Technology
Course: CET111 - Introduction to Computer and Programming
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        # Skip comments and empty lines
        if line and not line.startswith('#') and not line.startswith('-r'):
            # Remove inline comments
            if '#' in line:
                line = line[:line.index('#')].strip()
            if line:
                requirements.append(line)

setup(
    # Package Information
    name="medlink",
    version="1.0.0",
    description="Unified Medical Records System with NFC Smart Card Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Author Information
    author="Youssef",
    author_email="your.email@example.com",  # Update with your email
    
    # URLs
    url="https://github.com/yourusername/medlink",  # Update with your GitHub URL
    project_urls={
        "Bug Reports": "https://github.com/yourusername/medlink/issues",
        "Source": "https://github.com/yourusername/medlink",
        "Documentation": "https://github.com/yourusername/medlink/tree/main/docs",
    },
    
    # Package Discovery
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    
    # Python Version
    python_requires='>=3.9',
    
    # Dependencies
    install_requires=requirements,
    
    # Optional Dependencies
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
            'pylint>=3.0.3',
            'black>=23.12.1',
            'mypy>=1.7.1',
        ],
        'docs': [
            'sphinx>=7.2.6',
            'sphinx-rtd-theme>=2.0.0',
        ],
    },
    
    # Entry Points (CLI commands)
    entry_points={
        'console_scripts': [
            'medlink=main:main',  # Run 'medlink' command to start application
        ],
    },
    
    # Package Data
    include_package_data=True,
    package_data={
        'medlink': [
            'config/*.py',
            'data/*.json',
            'assets/**/*',
        ],
    },
    
    # Classifiers
    classifiers=[
        # Development Status
        'Development Status :: 4 - Beta',
        
        # Intended Audience
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        
        # Topic
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Office/Business',
        
        # License
        'License :: Other/Proprietary License',
        
        # Programming Language
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        
        # Operating System
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        
        # GUI Framework
        'Framework :: tkinter',
        
        # Natural Language
        'Natural Language :: English',
    ],
    
    # Keywords
    keywords='medical, healthcare, records, nfc, emergency, hospital, patient, doctor',
    
    # Zip Safe
    zip_safe=False,
)

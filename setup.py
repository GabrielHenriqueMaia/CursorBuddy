"""Project Sentinel - Agentic Loop for Windows Desktop Automation"""

from setuptools import setup, find_packages

setup(
    name="sentinel",
    version="0.1.0",
    description="Modular agentic assistant for Windows desktop automation",
    author="Project Sentinel",
    python_requires=">=3.10",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "openai>=1.0.0",
        "anthropic>=0.28.0",
        "google-generativeai>=0.3.0",
        "pywin32>=305",
        "Pillow>=10.0.0",
        "pytesseract>=0.3.10",
        "structlog>=24.0.0",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest-cov>=4.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sentinel=sentinel.cli:main",
        ]
    },
)

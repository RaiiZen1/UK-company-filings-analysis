"""A setup module for the xipeai package.

This module handles the setup configuration for the xipeai package, including
package metadata, finding packages, and installing requirements.
"""

from setuptools import find_packages, setup
from typing import List

# Constant for editable installations
HYPEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """Reads a requirements file and returns a list of requirements.

    Args:
        file_path: A string representing the path to the requirements file.

    Returns:
        A list of strings where each string is a package requirement.
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [
            req.strip()
            for req in requirements
            if req.strip() and req.strip() != HYPEN_E_DOT
        ]

    return requirements


setup(
    name="UK-Company-Filings-Analysis",
    version="1.0",
    author="Markus Herre",
    author_email="mherre@mail.uni-mannheim.de",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)

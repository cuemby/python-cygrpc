import pathlib, os
from setuptools import setup, find_packages
# from pathlib import Path
from typing import List


def parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    requirements: list = ""
    with open(os.getcwd() + '/' + filename) as file:
        requirements = file.readlines()
    requirements = [r.strip() for r in requirements]
    requirements = [r for r in sorted(requirements) if r and not r.startswith('#')]
    return requirements


# CyGRPC version
VERSION: str = '1.0.1.post1'
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README: str = (HERE / "README.md").read_text()

packages = find_packages()
packages.append("cygrpc")
# Setup
setup(
    name='cygrpc',
    version=VERSION,
    packages=packages,
    # package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    url='https://github.com/cuemby/python-cygrpc',
    license='MIT',
    author='Fabio Moreno',
    author_email='fabio.moreno@cuemby.com',
    description='gRPC Micro framework',
    long_description=README,
    long_description_content_type='text/markdown',
    setup_requires=['wheel', 'twine'],
    install_requires=[
        'wheel',
        'twine',
        'bottle',
        'Paste',
        'grpcio>=1.23.0',
        'grpcio-tools>=1.23.0',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'cygrpc = cygrpc.cli:main',
        ]
    },
    #    scripts=['bin/cygrpc.py']
)

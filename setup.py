from setuptools import setup, find_packages


with open(file='requirements.txt', mode='r') as file:
    requirements = [line.strip() for line in file.readlines()]

setup(
    name='rps',
    version='0.0.1',
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    install_requirements=requirements,
)

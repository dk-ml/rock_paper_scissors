#!/usr/bin/env python
from setuptools import find_packages, setup


NAME = "rock_paper_scissors"
VERSION = "0.0.1"
URL = "https://github.com/dk-ml/rock_paper_scissors"


with open(file="requirements.txt", mode="r") as file:
    requirements = [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        url=URL,
        packages=find_packages(exclude=["tests"]),
        install_requires=requirements,
        python_requires="~=3.6",
    )

from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
setup(
    name="utparking",
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages(),
)
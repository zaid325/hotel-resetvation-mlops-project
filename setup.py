from setuptools import setup , find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPs-Project-1-hotesl-reservation-prediction",
    version="0.1",
    aurthor="zaid kamran",
    packages=find_packages(),
    install_requires=requirements,
)
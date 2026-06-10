from setuptools import setup, find_packages

setup(
    name="genroute-security",
    version="1.0.0",
    description="AI-powered smart contract security pipeline for GenLayer",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "pytest>=7.4.0",
    ],
)

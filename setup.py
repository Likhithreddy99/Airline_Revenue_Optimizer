from setuptools import setup, find_packages

setup(
    name="airline-revenue-optimizer",
    version="0.1.0",
    description="My First END to END ML Project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
    ],
    python_requires=">=3.7",
)
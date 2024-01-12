from setuptools import setup, find_packages


setup(
    name="package name",
    version="0.0.1",
    author="Andrew Ryan",
    author_email="aryanvt15@proton.me",
    description="Tool decription",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["package = package.cli:main"],
    },
    install_requires=[
        "numpy",
        "pandas",
        "numba",
        "tqdm",
        "Pillow",
        "geopandas",
        "matplotlib",
        "affine",
        "numba",
        "psycopg2-binary",
        "sqlalchemy",
        "google-cloud-storage",
    ],
)

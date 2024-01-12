from setuptools import setup, find_packages


setup(
    name="geodbscan",
    version="0.0.1",
    author="Andrew Ryan",
    author_email="aryanvt15@proton.me",
    description="Implementation of DBSCAN for use with geospatial data.",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["geodbscan = geodbscan.cli:main"],
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
    ],
)

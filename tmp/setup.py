from setuptools import setup, find_packages

setup(
    name="asep",
    version="0.1.0",
    author="Vasilis Tsaknis",
    author_email="your.email@example.com",
    description="Script to give statistics about greek hiring in schools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vaionicle/asep",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # Dependencies
        "xlrd",
        "pandas",
        "openpyxl",

        "fastapi==0.95.1",
        "uvicorn==0.22.0",

        "psycopg2-binary",

        #new
        "SQLAlchemy>=2.0",
        "alembic",
        "python-dotenv",
        "mariadb"
    ],
    include_package_data=True,
)
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="risk_assessment_api",
    version="1.0.0",
    description="FastAPI-Service for risk assessment and workflow simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "fastapi",
        "risk assessment",
        "workflow simulation",
        "pydantic",
        "sqlalchemy",
    ],
    author="Ali Khalaji",
    author_email="khalaji.ali@gmx.de",
    url="https://github.com/alikhalajii/risk_assessment_api",
    packages=find_packages(exclude=["tests*", "data*"]),
    python_requires=">=3.8, <4",
    install_requires=[
        "fastapi==0.110.2",
        "pydantic==2.7.1",
        "python-multipart==0.0.9",
        "sqlalchemy==2.0.30",
        "uvicorn[standard]==0.29.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        ],
)

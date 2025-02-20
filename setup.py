from setuptools import setup, find_packages

setup(
    name="cpg2py",  
    version="1.0.3", 
    author="Yichao Xu",
    author_email="yxu166@jhu.edu",
    description="A graph-based data structure designed for querying CSV files in Joern format in Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YichaoXu/cpg2py",  
    packages=find_packages(include=["cpg2py", "cpg2py.*"]),
    install_requires=[],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
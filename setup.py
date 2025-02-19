from setuptools import setup, find_packages

setup(
    name="cpg2py",  # 你的包名
    version="1.0.0",  # 版本号
    author="Yichao Xu",
    author_email="yxu166@jhu.edu",
    description="A graph-based data structure designed for querying CSV files in Joern format in Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YichaoXu/cpg2py",  # GitHub 项目地址
    packages=find_packages(),
    install_requires=[],  # 你的包的依赖项（如果有）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
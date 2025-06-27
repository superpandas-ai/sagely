from setuptools import setup, find_packages

setup(
    name="superpython",
    version="0.0.1",
    description="LLM assistant for Python packages in REPLs and notebooks",
    author="SuperPandas Ltd",
    author_email="superpython@superpandas.ai",
    packages=find_packages(),
    install_requires=[
        "openai",
        "ipython",
        "pygments",
        "ipywidgets",
    ],
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
) 
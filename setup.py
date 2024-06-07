from setuptools import setup, find_packages

setup(
    name="mmo_market_tracker",
    version="0.1.0",
    description="A package for tracking and analyzing MMO market data",
    author="Gabriel Monteiro da Silva",
    author_email="gabriel.monteiro233@gmail.com",
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        "numpy"
        "pandas",
        "Pillow==10.3",
        "plotly",
        "pytesseract",
        "pywin32"
        "opencv-python"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
)
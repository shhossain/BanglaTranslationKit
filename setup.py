from setuptools import setup, find_packages

version = "0.0.1"
short_description = "BanglaTranslationKit is a collaborative open-source language translation package meticulously designed for smooth offline conversion between both Bangla and English languages (English to Bangla and Bangla to English)"
author = "shhossain"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

tags = [
    "bangla",
    "english",
    "translation",
    "nlp",
    "machine-translation",
    "bangla to english translation",
    "english to bangla translation",
]

classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Text Processing :: Linguistic",
    "License :: OSI Approved :: Apache-2.0 license",
    "Programming Language :: Python :: 3",
]
setup(
    name="bntrans",
    version=version,
    author=author,
    author_email="",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shhossain/BanglaTranslationKit",
    packages=find_packages(),
    install_requires=install_requires,
    keywords=tags,
    classifiers=classifiers,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "bntrans = bntrans.cli:main",
        ],
    },
)

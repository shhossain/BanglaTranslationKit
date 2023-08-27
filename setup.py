from setuptools import setup, find_packages

version = "0.0.4"
short_description = "BanglaTranslationKit: Open-source tool for offline Bangla-English translation."
author = "shhossain"

with open("README.md", "r", encoding="utf-8") as fh:
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
    "Topic :: Text Processing :: Linguistic",
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

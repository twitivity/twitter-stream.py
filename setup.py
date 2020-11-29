from os.path import dirname, abspath, join
from setuptools import setup

NAME: str = "twitter-stream.py"
AUTHOR: str = "Saadman Rafat"
DESCRIPTION: str = "Python Client For Twitter Streaming API v2"
URL: str = "https://github.com/twitivity/twitter-stream.py"
REQUIRES_PYTHON: str = ">=3.6.0"
VERSION = "0.4.0"
REQUIRED = ["requests"]
EMAIL = "saadmanhere@gmail.com"

with open(join(abspath(dirname(__file__)), "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license="MIT",
    install_requires=REQUIRED,
    include_package_data=True,
    py_modules=["twitter_stream"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)

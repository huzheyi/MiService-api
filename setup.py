#!/usr/bin/env python3

import os
import sys

if len(sys.argv) == 1:
    os.system("%s sdist" % sys.argv[0])
    os.system("twine upload dist/*")
    os.system("rm -rf dist *.egg-info")
    exit(0)


from setuptools import setup

setup(
    name="miservice_fork",
    description="XiaoMi Cloud Service fork from https://github.com/yihong0618/MiService",
    version="2.7.1",
    license="MIT",
    author="Yonsm, yihong0618, huzheyi",
    author_email="Yonsm@qq.com, zouzou0208@gmail.com, huzheyi@msn.com",
    url="https://github.com/huzheyi/MiService-api.git",
    packages=["miservice"],
    scripts=["micli.py"],
    python_requires=">=3.8",
    install_requires=["aiohttp", "mutagen", "rich", "fastapi", "pydantic", "uvicorn"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["micli = miservice.cli:micli"],
    },
)

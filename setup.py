# -*- coding: utf-8 -*-
"""
Created on Fri May 24 22:44:08 2019

@author: tefpo
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Oanda Historical Data Fetcher",
    version="0.0.1",
    author="Tomasz Posluszny",
    author_email="tefposluszny@gmail.com",
    description="Download historical data from Oanda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alucarded/oanda_fetcher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
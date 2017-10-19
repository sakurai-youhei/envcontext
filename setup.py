'''
Created on 2017/10/17

@author: sakurai
'''
from os import getenv

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from textwrap import dedent


BUILD = getenv("APPVEYOR_BUILD_NUMBER")
HOMEPAGE = "https://github.com/sakurai-youhei/envcontext"
setup(
    version="2017.10.19" + (BUILD and ".{}".format(BUILD) or ""),
    name="envcontext",
    py_modules=["envcontext"],
    license="MIT",
    maintainer="Youhei Sakurai",
    maintainer_email="sakurai.youhei@gmail.com",
    url=HOMEPAGE,
    description=("Context manager to update environment variables with "
                 "preservation"),
    long_description="See README on %s" % HOMEPAGE,
    classifiers=dedent("""\
        License :: OSI Approved :: MIT License
        Development Status :: 5 - Production/Stable
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Intended Audience :: Developers
    """).splitlines(),
    keywords=dedent("""\
        Context Manager
        Environmental Variable
    """).splitlines(),
)

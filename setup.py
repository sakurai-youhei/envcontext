'''
Created on 2017/10/17

@author: sakurai
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from textwrap import dedent


HOMEPAGE = "https://github.com/sakurai-youhei/envcontext"
setup(
    version="2017.10.17",
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
        Development Status :: 4 - Beta
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

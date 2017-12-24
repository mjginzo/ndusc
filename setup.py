"""Setup file.

File that allows to install the ndusc package.
"""
from setuptools import setup, find_packages


# readme ----------------------------------------------------------------------
def readme():
    """Load README.md file."""
    with open('README.md') as f:
        return f.read()
# --------------------------------------------------------------------------- #


# license ---------------------------------------------------------------------
def license():
    """Return LICENSE file information."""
    with open('LICENSE') as f:
        return f.read()
# --------------------------------------------------------------------------- #


# requirements ----------------------------------------------------------------
def requirements():
    """Return requirements.txt file information."""
    with open('requirements.txt') as f:
        return f.read()
# --------------------------------------------------------------------------- #


# Dependency links
# ================
# Ex.: 'svn+http://mares.usc.es/svn/heisenberg/projects/pyutils#egg=pyutils'
dependency_links = []


# Description
# ===========
description = """Nested decomposition algorithm.

Implementation done by the University of Santiago de Compostela (USC), Spain.

The tool is implemented to solve linear multistage stochastic programs. The
subproblems must have continuous variables, but also our implementation can
solve problem with binary variables if all variables in a subproblem are of the
same type (continuous or binary).
"""

# setup
# =====
setup(
    name='ndusc',
    version='0.0.1',
    author='Jorge Rodriguez-Veiga, David Rodriguez-Penas',
    author_email='jorge.rodriguez.veiga@usc.es, david.rodriguez.penas@usc.es',
    description=description,
    classifiers=['Programming Language :: Python :: 3.6'],
    long_description=readme(),
    packages=find_packages(),
    install_requires=requirements(),
    include_package_data=True,
    license=license(),
    dependency_links=dependency_links,
    entry_points={'console_scripts': ['ndusc=ndusc.main:main']}
)

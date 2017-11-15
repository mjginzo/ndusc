from setuptools import setup, find_packages

# README.md file
# ==============
def readme():
    with open('README.md') as f:
        return f.read()


# LICENSE file
# ============
def license():
    with open('LICENSE') as f:
        return f.read()


# requirements.txt file
# =====================
def requirements():
    with open('requirements.txt') as f:
        return f.read()


# Dependency links
# ================
# Example: 'svn+http://mares.usc.es/svn/heisenberg/projects/pyutils#egg=pyutils'
dependency_links=[
]

# Description
# ===========
description = '''
'''

# setup
# =====
setup(
    name = 'nested_decomposition',
    version = '0.0.1',
    author = '',
    author_email = '',
    description = description,
    classifiers = ['Programming Language :: Python :: 2.7'],
    long_description = readme(),
    packages = find_packages(),
    install_requires = requirements(),
    include_package_data=True,
    license = license(),
    dependency_links = dependency_links,
)
# -*- coding: utf-8 -*-
"""Package namespace.

This package structure is compatible with Python2 and Python3.
"""

# Python packages
import importlib as _importlib
import pkgutil as _pkgutil


# _import_submodules ----------------------------------------------------------
def _import_submodules(package, recursive=True):
    """Import all submodules of a module, recursively, including subpackages.

    Args:
        package (:obj:`str`): package (name or actual module).
        recursive (:obj:`bool`): ``True`` to import subpackages.

    Return:
        :obj:`dict`: dictionary with package information.
    """
    if isinstance(package, str):
        package = _importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in _pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = _importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(_import_submodules(full_name))
    return results
# --------------------------------------------------------------------------- #


# Execute the _import_submodules function to load the package.
_import_submodules(__name__)

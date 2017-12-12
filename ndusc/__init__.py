"""Package namespace."""
import importlib as _importlib
import pkgutil as _pkgutil


def import_submodules(package, recursive=True):
    """Import all submodules of a module, recursively, including subpackages.

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = _importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in _pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = _importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


import_submodules(__name__)

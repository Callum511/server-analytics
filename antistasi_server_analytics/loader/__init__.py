
import inspect
from pathlib import Path

import pkgutil
from traceback import print_tb
import sys
import importlib
from types import ModuleType
from ._base_loader import BaseLoader
from ._loader_collector import LoaderContainer


def _extract_loaders_from_module(name: str) -> ModuleType:

    def _predicate(in_object: object) -> bool:
        return inspect.isclass(in_object) and not inspect.isabstract(in_object) and issubclass(in_object, BaseLoader)

    module = importlib.import_module(name)
    for loader_class_name, loader_class_object in inspect.getmembers(module, predicate=_predicate):
        yield loader_class_object


def _import_data_loaders_from_folder() -> frozenset["BaseLoader"]:

    all_loaders = set()

    for sub_module in pkgutil.walk_packages(__path__, __name__ + '.', onerror=print_tb):
        for _loader_class in _extract_loaders_from_module(sub_module.name):
            all_loaders.add(_loader_class)

    return frozenset(all_loaders)


LOADER_CONTAINER = LoaderContainer()
ALL_LOADER = _import_data_loaders_from_folder()


LOADER_CONTAINER.add_loaders(ALL_LOADER)

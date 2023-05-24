from ._base_loader import BaseLoader
from ._loader_collector import LoaderContainer

from .json_loader import JsonLoader
from .folder_loader import FolderLoader
from .zip_loader import ZipLoader
from .csv_loader import CSVLoader


def _initialize_loader_container() -> LoaderContainer:
    """
    CURRENTLY UNUSED!


    """

    def all_subclasses_recursively(klass: type) -> set[type]:
        return set(klass.__subclasses__()).union([s for c in klass.__subclasses__() for s in all_subclasses_recursively(c)])

    loader_collector = LoaderContainer()
    for sub_class in all_subclasses_recursively(BaseLoader):
        loader_collector.add_loader(sub_class)

    return loader_collector


LOADER_CONTAINER = LoaderContainer()
LOADER_CONTAINER.add_loader(JsonLoader)
LOADER_CONTAINER.add_loader(FolderLoader)
LOADER_CONTAINER.add_loader(ZipLoader)
LOADER_CONTAINER.add_loader(CSVLoader)

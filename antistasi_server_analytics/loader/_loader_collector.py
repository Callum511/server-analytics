"""
WiP.

Soon.
"""

# region [Imports]


import inspect


from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)


from sortedcontainers import SortedDict, SortedList, SortedSet

import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from ._base_loader import BaseLoader
if TYPE_CHECKING:
    ...

# endregion [Imports]


# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


def _loader_sort_key(loader_class) -> int:
    return - inspect.getattr_static(loader_class, "specificity", 1)


T_LOADER_CLASS = TypeVar("T_LOADER_CLASS", bound=BaseLoader)


class LoaderContainer:

    def __init__(self) -> None:
        self._all_loader: SortedSet[BaseLoader] = SortedSet(key=_loader_sort_key)
        self._file_loader_extension_map: defaultdict[str, SortedSet[BaseLoader]] = defaultdict(lambda: SortedSet(key=_loader_sort_key))

    def add_loader(self, loader_class: T_LOADER_CLASS) -> T_LOADER_CLASS:
        if not issubclass(loader_class, BaseLoader):
            raise TypeError(f"Only loader that subclass {BaseLoader.__name__!r} can be added to {self.__class__.__name__!r}")

        self._all_loader.add(loader_class)

        try:
            for file_extension in loader_class.file_extensions:

                self._file_loader_extension_map[file_extension].add(loader_class)
        except AttributeError:
            pass

        loader_class.loader_container = self
        return loader_class

    def add_loaders(self, loader_classes: Iterable["BaseLoader"]) -> Self:
        for loader_class in loader_classes:
            self.add_loader(loader_class)

        return self

    def determine_loader(self, item: object) -> type[BaseLoader]:
        try:
            item_path = Path(item).resolve()
            for file_loader in self._file_loader_extension_map[item_path.suffix]:
                if file_loader.can_load(item_path) is True:
                    return file_loader

        except (TypeError, KeyError):
            for loader_class in self._all_loader:
                if loader_class.can_load(item) is True:
                    return loader_class

        raise RuntimeError(f"Unable to determine loader for item {item!r}.")

    def create_loader(self, item: object) -> BaseLoader:
        return self.determine_loader(item)(source=item)


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

"""
WiP.

Soon.
"""

# region [Imports]

import os


from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)


from ._base_loader import BaseLoader

from antistasi_server_analytics.data_types import ConnectionEntry

if TYPE_CHECKING:
    from antistasi_server_analytics.data_types.aux_data_types import AuxCache


# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class FolderLoader(BaseLoader):
    __slots__ = ("_sub_items", "_sub_loader")
    specificity = 5
    file_extensions: tuple[str] = ("",)
    has_sub_loader: bool = True

    def __init__(self, source: Union[str, os.PathLike, Path]):
        self._source = Path(source).resolve()
        self._sub_items: set[Path] = self._get_sub_items()

    @property
    def source_name(self) -> str:
        return str(self._source.name)

    def amount_connection_data_items(self) -> int:
        return len(self._sub_items)

    def _is_sub_item(self, item: Path) -> bool:
        if item.is_dir() is True:
            return False

        return True

    def _get_sub_items(self) -> set[Path]:
        sub_items = set()
        for dirname, folderlist, filelist in os.walk(self._source):
            for file in filelist:
                item = Path(dirname, file).resolve()
                if self._is_sub_item(item):
                    sub_items.add(item)
        return sorted(sub_items)

    def _iter_subloader(self) -> Generator[BaseLoader, None, None]:
        for item in self._sub_items:
            sub_loader = self.loader_container.create_loader(item)
            yield from sub_loader.get_resolved_loaders()

    def iter_entries(self, cache: "AuxCache" = None) -> Generator["ConnectionEntry", None, None]:
        for loader in self._sub_loader:
            yield from loader.iter_entries(cache=cache)

    def get_resolved_loaders(self) -> list[BaseLoader]:
        return list(self._iter_subloader())

    @ classmethod
    def can_load(cls, input_item: object) -> bool:
        try:
            input_path = Path(input_item).resolve()

            if input_path.is_dir() is True:
                return True

        except TypeError:
            return False

        return False

# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

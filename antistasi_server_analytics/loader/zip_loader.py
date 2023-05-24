"""
WiP.

Soon.
"""

# region [Imports]

import os


from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)
from zipfile import ZipFile, ZIP_LZMA, ZipInfo


from ._base_loader import BaseLoader

from antistasi_server_analytics.data_types import ConnectionEntry

if TYPE_CHECKING:
    ...

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class ZipLoader(BaseLoader):
    __slots__ = tuple()
    specificity = 5
    file_extensions: tuple[str] = (".zip",)

    def __init__(self, source: Union[str, os.PathLike, Path]):
        self._source = Path(source).resolve()

    def _get_sub_items(self) -> set[Path]:
        sub_items = set()
        for dirname, folderlist, filelist in os.walk(self._source):
            for file in filelist:
                item = Path(dirname, file).resolve()
                if self._is_sub_item(item):
                    sub_items.add(item)
        return sub_items

    def _iter_sub_items(self) -> Generator[tuple[bytes, str], None, None]:
        with ZipFile(self._source, "r") as zippy:
            for item_info in zippy.filelist:
                item_info: ZipInfo
                if item_info.is_dir() is True:
                    continue
                yield zippy.read(item_info), os.path.splitext(item_info.filename)[-1]

    def _iter_sub_loader(self) -> Generator[BaseLoader, None, None]:
        for data, suffix in self._iter_sub_items():
            yield self.loader_container._file_loader_extension_map[suffix][0](data)

    def iter_entries(self) -> Generator["ConnectionEntry", None, None]:
        for loader in self._iter_sub_loader():
            yield from loader.iter_entries()

    @classmethod
    def can_load(cls, input_item: object) -> bool:
        try:
            input_path = Path(input_item).resolve()

            if input_path.is_file() is True and input_path.suffix in cls.file_extensions:
                return True

        except TypeError:
            return False

        return False

# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

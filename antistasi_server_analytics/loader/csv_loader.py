"""
WiP.

Soon.
"""

# region [Imports]

import os

import sys


from pathlib import Path


from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)

from antistasi_server_analytics.data_types import ConnectionEntry

import csv

from antistasi_server_analytics.loader._base_loader import BaseLoader


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


class CSVLoader(BaseLoader):
    __slots__ = tuple()
    specificity = 2
    file_extensions: tuple[str] = (".csv",)
    delimiter: str = ","
    quote_char: str = "|"

    def __init__(self, source: Union[str, os.PathLike, Path, bytes]):
        if isinstance(source, bytes):
            self._source = source
        else:
            self._source = Path(source).resolve()

    def amount_connection_data_items(self) -> int:
        if isinstance(self._source, bytes):
            return len(self._source.decode(encoding='utf-8', errors='ignore').splitlines()) - 1

        elif isinstance(self._source, Path):
            return len(self._source.read_text(encoding='utf-8', errors='ignore').splitlines()) - 1

    def _iter_from_path(self, cache: "AuxCache" = None) -> Generator[ConnectionEntry, None, None]:
        with self._source.open("r", encoding='utf-8', errors='ignore', newline="") as f:
            csv_reader = csv.DictReader(f, delimiter=self.delimiter, quotechar=self.quote_char)

            yield from (ConnectionEntry.from_dict(row, cache=cache) for row in csv_reader)

    def _iter_from_bytes(self, cache: "AuxCache" = None) -> Generator[ConnectionEntry, None, None]:
        csv_reader = csv.DictReader(self._source.decode(encoding='utf-8', errors='ignore').splitlines(), delimiter=self.delimiter, quotechar=self.quote_char)
        yield from (ConnectionEntry.from_dict(row, cache=cache) for row in csv_reader)

    def iter_entries(self, cache: "AuxCache" = None) -> Generator[ConnectionEntry, None, None]:
        if isinstance(self._source, bytes):
            yield from self._iter_from_bytes(cache=cache)

        else:
            yield from self._iter_from_path(cache=cache)

    def get_resolved_loaders(self) -> list[BaseLoader]:
        return [self]

    @classmethod
    def can_load(cls, input_item: object) -> bool:
        try:
            input_path = Path(input_item).resolve()

            if input_path.suffix in cls.file_extensions:
                return True

        except TypeError:
            return False

        return False


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]
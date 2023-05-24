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

from antistasi_server_analytics.data_types import ConnectionEntry


try:
    import orjson as json
except ImportError:
    import json

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


class JsonLoader(BaseLoader):
    __slots__ = tuple()
    specificity = 2
    file_extensions: tuple[str] = (".json",)

    def __init__(self, source: Union[str, os.PathLike, Path, bytes]):
        if isinstance(source, bytes):
            self._source = source
        else:
            self._source = Path(source).resolve()

    def _iter_from_path(self) -> Generator[ConnectionEntry, None, None]:
        with self._source.open("rb") as binary_f:
            yield from (ConnectionEntry.from_dict(item) for item in json.loads(binary_f.read()))

    def _iter_from_bytes(self) -> Generator[ConnectionEntry, None, None]:
        yield from (ConnectionEntry.from_dict(item) for item in json.loads(self._source))

    def iter_entries(self) -> Generator[ConnectionEntry, None, None]:
        if isinstance(self._source, bytes):
            yield from self._iter_from_bytes()

        else:
            yield from self._iter_from_path()

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

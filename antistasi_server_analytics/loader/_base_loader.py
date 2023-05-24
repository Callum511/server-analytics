"""
WiP.

Soon.
"""

# region [Imports]


from abc import ABC, abstractmethod

from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)


if TYPE_CHECKING:
    from antistasi_server_analytics.loader._loader_collector import LoaderContainer
    from antistasi_server_analytics.data_types import ConnectionEntry, PlayerDataContainer

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


T_PLAYER_CONTAINER = TypeVar("T_PLAYER_CONTAINER", bound="PlayerDataContainer")


class BaseLoader(ABC):
    __slots__ = ("_source",)
    loader_container: "LoaderContainer" = None

    def __init__(self, source: object):
        self._source = source

    @classmethod
    @abstractmethod
    def can_load(cls, input_item: object) -> bool:
        ...

    @abstractmethod
    def iter_entries(self) -> Generator["ConnectionEntry", None, None]:
        ...

    def add_to_player_container(self, player_container: T_PLAYER_CONTAINER, data_filter: Callable[["ConnectionEntry"], bool] = None) -> T_PLAYER_CONTAINER:
        if data_filter is None:

            for entry in self.iter_entries():
                player_container.add_data(entry)

        else:
            for entry in self.iter_entries():
                if data_filter(entry) is True:
                    player_container.add_data(entry)

        return player_container

# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

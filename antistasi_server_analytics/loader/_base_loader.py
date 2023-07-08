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
from contextlib import nullcontext
from threading import Lock, RLock
if TYPE_CHECKING:
    from antistasi_server_analytics.loader._loader_collector import LoaderContainer
    from antistasi_server_analytics.data_types import ConnectionEntry, PlayerDataContainer
    from antistasi_server_analytics.data_types.aux_data_types import AuxCache

    from rich.progress import Task, Progress
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
    has_sub_loader: bool = False
    concurrent_priority: int = 10

    def __init__(self, source: object):
        self._source = source

    @property
    def source_name(self) -> str:
        return str(self._source)

    @classmethod
    @abstractmethod
    def can_load(cls, input_item: object) -> bool:
        ...

    @abstractmethod
    def amount_connection_data_items(self) -> int:
        ...

    @abstractmethod
    def iter_entries(self, cache: "AuxCache" = None) -> Generator["ConnectionEntry", None, None]:
        ...

    @abstractmethod
    def get_resolved_loaders(self) -> list["BaseLoader"]:
        ...

    def add_to_player_container(self,
                                player_container: T_PLAYER_CONTAINER,
                                data_filter: Callable[["ConnectionEntry"], bool] = None,
                                progress_bar: "Progress" = None,
                                progress_task_id: int = None) -> T_PLAYER_CONTAINER:

        if progress_bar is not None:
            progress_bar.reset(progress_task_id, total=self.amount_connection_data_items(), description=f"loading from {self.source_name!r}...")
            # progress_bar.update(progress_task_id, total=self.amount_connection_data_items())
        cache = player_container._aux_cache
        if data_filter is None:

            for entry in self.iter_entries(cache=cache):
                if entry.name != "__SERVER__":

                    player_container.add_data(entry)
                    if progress_bar is not None:
                        progress_bar.advance(progress_task_id)
        else:
            for entry in self.iter_entries(cache=cache):
                if entry.name != "__SERVER__":

                    if data_filter(entry) is True:

                        player_container.add_data(entry)
                    if progress_bar is not None:
                        progress_bar.advance(progress_task_id, advance=1)
        return player_container

    def __len__(self) -> int:
        return self.amount_connection_data_items()
# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

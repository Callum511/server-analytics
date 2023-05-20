"""
WiP.
"""

# region [Imports]


from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from datetime import datetime, timezone, timedelta
import heapq
from sortedcontainers import SortedSet
from antistasi_server_analytics.data_types.connection_entry import ConnectionEntry

if TYPE_CHECKING:
    ...

# endregion [Imports]

# region [Logging]


# endregion [Logging]

# region [Constants]


# endregion [Constants]

class PlayerData:

    __slots__ = ("steamid",
                 "connections")

    def __init__(self,
                 steamid: str) -> None:

        self.steamid = steamid
        self.connections: SortedSet["ConnectionEntry"] = SortedSet()

    @property
    def names(self) -> set[str]:
        return set(i.name for i in self.connections)

    @property
    def last_used_name(self) -> Optional[str]:
        try:
            return self.connections[-1].name
        except IndexError:
            return None

    @property
    def first_used_name(self) -> Optional[str]:
        try:
            return self.connections[0].name
        except IndexError:
            return None

    @property
    def first_connection(self) -> Optional["ConnectionEntry"]:
        try:
            return self.connections[0]
        except IndexError:
            return None

    @property
    def last_connection(self) -> Optional["ConnectionEntry"]:
        try:
            return self.connections[-1]
        except IndexError:
            return None

    @property
    def amount_connections(self) -> int:
        return len(self.connections)

    @property
    def seen24h(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=24))

    @property
    def seen7d(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=7))

    @property
    def seen30d(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=30))

    def add_connection(self, new_connection: "ConnectionEntry") -> None:
        self.connections.add(new_connection)

    def __str__(self) -> str:
        return f"{self.steamid}(" + ', '.join(f"{name!r}" for name in self.names) + ")"

    def __repr__(self):
        attr = {attr_name: getattr(self, attr_name) for attr_name in (self.__slots__ + ("first_connection", "last_connection"))}

        return ', '.join(f"{name}={value!r}" for name, value in attr.items())


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]

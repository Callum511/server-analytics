"""
WiP.
"""

# region [Imports]


from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from datetime import datetime, timezone, timedelta
import heapq
from sortedcontainers import SortedSet, SortedList
from collections import defaultdict
from antistasi_server_analytics.data_types.connection_entry import ConnectionEntry, ConnectionType
import dataclasses
from weakref import proxy, ReferenceType, ProxyType
from pathlib import Path
from functools import total_ordering
from antistasi_server_analytics.misc.output_helper import make_renderable_simple_dict
if TYPE_CHECKING:
    from antistasi_server_analytics.data_types.player_data_container import PlayerDataContainer
    from rich.console import Console, ConsoleOptions, RenderResult

# endregion [Imports]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class PlayerData:

    __slots__ = ("player_data_container",
                 "steamid",
                 "connections",
                 "disconnections")

    def __init__(self,
                 steamid: str,
                 player_data_container: "PlayerDataContainer") -> None:
        self.player_data_container: "PlayerDataContainer" = proxy(player_data_container)
        self.steamid = steamid
        self.connections: SortedSet["ConnectionEntry"] = SortedSet()
        self.disconnections: SortedSet["ConnectionEntry"] = SortedSet()

    @property
    def steam_id(self) -> str:
        return self.steamid

    @property
    def all_connection_data(self) -> SortedSet["ConnectionEntry"]:
        return self.connections.union(self.disconnections)

    @property
    def now_time(self) -> datetime:
        return self.player_data_container.now_time

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
    def amount_disconnections(self) -> int:
        return len(self.disconnections)

    @property
    def amount_connection_data_combined(self) -> int:
        return len(self.all_connection_data)

    @property
    def is_connections_disconnections_balanced(self) -> bool:
        return len(self.connections) == len(self.disconnections)

    @property
    def seen24h(self):
        if self.last_connection is not None:
            return self.last_connection.recorded_at > (self.now_time - timedelta(hours=24))
        return False

    @property
    def seen7d(self):
        if self.last_connection is not None:
            return self.last_connection.recorded_at > (self.now_time - timedelta(days=7))
        return False

    @property
    def seen30d(self):
        if self.last_connection is not None:
            return self.last_connection.recorded_at > (self.now_time - timedelta(days=30))

        return False

    def add_connection_data(self, new_connection_data: "ConnectionEntry") -> None:

        if new_connection_data.connection_type is ConnectionType.CONNECTED:
            self.connections.add(new_connection_data)

        elif new_connection_data.connection_type is ConnectionType.DISCONNECTED:
            self.disconnections.add(new_connection_data)

        else:
            raise RuntimeError(f"unknown connection_type {new_connection_data.connection_type!r} in {new_connection_data!r}")

    def __str__(self) -> str:
        return f"{self.steamid}(" + ', '.join(f"{name!r}" for name in self.names) + ")"

    def __repr__(self):
        attr = {attr_name: getattr(self, attr_name) for attr_name in (self.__slots__ + ("first_connection", "last_connection"))}

        return ', '.join(f"{name}={value!r}" for name, value in attr.items())

    def __rich_console__(self,
                         console: "Console",
                         options: "ConsoleOptions") -> "RenderResult":
        data = {}
        for attr_name in ("steam_id", "names", "amount_connections", "amount_disconnections", "amount_connection_data_combined", "is_connections_disconnections_balanced",
                          "first_connection", "last_connection", "seen24h", "seen7d", "seen30d", "last_used_name"):
            data[attr_name] = getattr(self, attr_name)

        yield make_renderable_simple_dict(data, title=self.__class__.__name__)
# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

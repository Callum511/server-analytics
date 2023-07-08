"""
WiP.
"""

# region [Imports]


from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from antistasi_server_analytics.data_types.player_data import PlayerData
from statistics import mean, mode, median, multimode, stdev, quantiles
import datetime
from sortedcontainers import SortedList
from weakref import proxy, ReferenceType
from antistasi_server_analytics.data_types.connection_entry import ConnectionEntry, ConnectionType
from itertools import chain
from antistasi_server_analytics.data_types.aux_data_types import AuxCache
from threading import Lock, RLock
if TYPE_CHECKING:
    from antistasi_server_analytics.application_context import ApplicationContext

# endregion [Imports]

# region [Logging]


# endregion [Logging]

# region [Constants]


# endregion [Constants]

class PlayerDataContainer:
    __slots__ = ("__weakref__",
                 "_now_time",
                 "steamid_to_player_data_map",
                 "_aux_cache",
                 "_data_lock")

    def __init__(self,
                 now_time: Union[datetime.datetime, str]) -> None:
        self._now_time = now_time
        self.steamid_to_player_data_map: dict[str, "PlayerData"] = {}
        self._aux_cache = AuxCache()
        self._data_lock = Lock()

    @property
    def now_time(self) -> datetime.datetime:
        if isinstance(self._now_time, str):
            if self._now_time == "LAST_ENTRY":
                self._now_time = max(i.recorded_at for i in self.all_connections)

            elif self._now_time == "REAL_NOW":
                self._now_time = datetime.datetime.now(tz=datetime.timezone.utc)

            else:
                self._now_time = datetime.datetime.fromisoformat(self._now_time).replace(tzinfo=datetime.timezone.utc)

        return self._now_time

    @property
    def players(self) -> list["PlayerData"]:
        return list(self.steamid_to_player_data_map.values())

    @property
    def all_connections(self) -> SortedList["ConnectionEntry"]:
        return SortedList(chain.from_iterable(p.connections for p in self.steamid_to_player_data_map.values()))

    @property
    def all_disconnections(self) -> SortedList["ConnectionEntry"]:
        return SortedList(chain.from_iterable(p.disconnections for p in self.steamid_to_player_data_map.values()))

    @property
    def amount_all_connections(self) -> int:
        return sum(len(p.connections) for p in self.players)

    def add_data(self, data: "ConnectionEntry") -> None:
        with self._data_lock:
            player = self.get_or_create_from_entry(data)
            player.add_connection_data(data)

    def get(self, steamid) -> Optional["PlayerData"]:
        return self.steamid_to_player_data_map.get(steamid)

    def get_or_create_from_entry(self, entry: "ConnectionEntry") -> "PlayerData":
        try:
            return self.steamid_to_player_data_map[entry.steamid]
        except KeyError:
            player = PlayerData(steamid=entry.steamid, player_data_container=self)
            self.steamid_to_player_data_map[player.steamid] = player
            return player

    def get_all(self) -> list["PlayerData"]:
        return self.players

    def get_all_sorted(self, sort_by, reverse=False) -> list["PlayerData"]:
        return sorted(self.players, key=lambda x: getattr(x, sort_by), reverse=reverse)

    def __getitem__(self, steamid: str) -> "PlayerData":
        return self.steamid_to_player_data_map[steamid]

    def average_amount_connections(self, round_n: int = 2) -> float:
        result = mean(i.amount_connections for i in self.players)
        if round_n is not None:
            result = round(result, ndigits=round_n)

        return result

    def median_amount_connections(self) -> float:
        return median(i.amount_connections for i in self.players)

    def mode_amount_connections(self) -> int:
        return mode(i.amount_connections for i in self.players)

    def multimode_amount_connections(self) -> list[int]:
        return multimode(i.amount_connections for i in self.players)

    def stdev_amount_connections(self, round_n: int = 2) -> float:
        result = stdev(i.amount_connections for i in self.players)
        if round_n is not None:
            result = round(result, ndigits=round_n)

        return result

    def quantiles_amount_connections(self) -> list[float]:
        return quantiles(i.amount_connections for i in self.players)

    def amount_unique_all_time(self) -> int:
        return len(self.players)

    def amount_unique_24h(self) -> int:

        return len({p for p in self.players if p.last_connection is not None and p.seen24h})

    def amount_unique_7d(self) -> int:

        return len({p for p in self.players if p.last_connection is not None and p.seen7d})

    def new30d(self) -> list["PlayerData"]:

        return [p for p in self.players if p.seen30d]


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]

"""
WiP.
"""

# region [Imports]


from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from antistasi_server_analytics.data_types.player_data import PlayerData
from statistics import mean, mode, median
import datetime
from antistasi_server_analytics.data_types.connection_entry import ConnectionEntry, ConnectionType

if TYPE_CHECKING:
    ...

# endregion [Imports]

# region [Logging]


# endregion [Logging]

# region [Constants]


# endregion [Constants]

class PlayerDataContainer:
    __slots__ = ("steamid_to_player_data_map",)

    def __init__(self) -> None:
        self.steamid_to_player_data_map: dict[str, "PlayerData"] = {}

    @property
    def players(self) -> list["PlayerData"]:
        return list(self.steamid_to_player_data_map.values())

    def add_data(self, data: "ConnectionEntry") -> None:
        player = self.get(data.steamid, create_if_missing=True)
        player.add_connection(data)

    def get(self, steamid, create_if_missing: bool = True) -> Optional["PlayerData"]:
        try:
            return self.steamid_to_player_data_map[steamid]
        except KeyError:
            if create_if_missing is True:
                player = PlayerData(steamid)
                self.steamid_to_player_data_map[player.steamid] = player
                return player

            else:
                return None

    def get_all(self) -> list["PlayerData"]:
        return self.players

    def get_all_sorted(self, sort_by, reverse=False) -> list["PlayerData"]:
        return sorted(self.players, key=lambda x: getattr(x, sort_by), reverse=reverse)

    def average_amount_connections(self) -> int:
        return mean(i.amount_connections for i in self.players)

    def median_amount_connections(self) -> int:
        return median(i.amount_connections for i in self.players)

    def mode_amount_connections(self) -> int:
        return mode(i.amount_connections for i in self.players)

    def amount_unique_all_time(self) -> int:
        return len(self.players)

    def amount_unique_24h(self) -> int:

        return len({p for p in self.players if p.seen24h})

    def amount_unique_7d(self) -> int:

        return len({p for p in self.players if p.seen7d})

    def new30d(self) -> list["PlayerData"]:
        date_30d_ago = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
        return [p for p in self.players if p.seen30d and (p.first_connection > date_30d_ago)]


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]

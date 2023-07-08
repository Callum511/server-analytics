"""
WiP
"""

# region [Imports]

import datetime
from typing import Any, Union, Optional, Generator, TypedDict, Mapping, Protocol, runtime_checkable, TextIO, BinaryIO, TYPE_CHECKING, NamedTuple
import dataclasses
import enum
from functools import total_ordering
from rich.table import Table
from rich.tree import Tree
from antistasi_server_analytics.misc.output_helper import make_renderable_simple_dict
from rich.scope import render_scope
from rich.box import HEAVY_EDGE, DOUBLE_EDGE
from rich.text import Text
from rich.console import Group
from rich.panel import Panel
from rich.pretty import Pretty
from antistasi_server_analytics.data_types.aux_data_types import Server, LogFile, GameMap, CampaignId, AntistasiVersion, Mod, ModList, AuxCache


import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult

# endregion [Imports]

# region [Logging]


# endregion [Logging]

# region [Constants]


# endregion [Constants]


@enum.unique
class ConnectionType(enum.Enum):
    CONNECTING = 10
    CONNECTED = 11

    DISCONNECTING = 20
    DISCONNECTED = 21

    @property
    def is_connecting_sub_type(self) -> bool:
        """
        Checks if it is part of the `connecting` process.

        `connecting`-process types have a value between `10` and `19`.
        """
        return self.value >= 10 and self.value < 20

    @property
    def is_disconnecting_sub_type(self) -> bool:
        """
        Checks if it is part of the `disconnecting` process.

        `disconnecting`-process types have a value between `20` and `29`.
        """
        return self.value >= 20 and self.value < 30

    @classmethod
    def _missing_(cls, value: object) -> Any:
        """
        Overwritten to handle input strings caseINsensitive.
        """
        if isinstance(value, str):
            try:
                return cls._member_map_[value.upper()]
            except KeyError:
                pass

            try:
                return {k.casefold(): v for k, v in cls.__members__.items()}[value.casefold()]
            except KeyError:
                pass

        return super()._missing_(value)

    def __str__(self) -> str:
        return self.name

    def __rich_console__(self,
                         console: "Console",
                         options: "ConsoleOptions") -> "RenderResult":
        yield (Text(self.__class__.__name__, style="inspect.class") + Text(".") + Text(self.name, style="repr.attrib_name"))

    def __rich__(self) -> str:
        return f"[b u]{self.__class__.__name__}[/b u].[magenta]{self.name}[/magenta]"


class ArrayData(NamedTuple):
    direct_play_id: Union[int, None] = None
    uid: Union[str, None] = None
    name: Union[str, None] = None
    jip: Union[bool, None] = None
    unknown_number: Union[int, None] = None
    owner: Union[int, None] = None

    @classmethod
    def new_array_data(cls, *values) -> Self:
        if len(values) <= 0:
            return cls()

        try:
            _direct_play_id = int(values[0])
        except (IndexError, ValueError):
            _direct_play_id = None

        try:
            _uid = sys.intern(values[1])
        except IndexError:
            _uid = None

        try:
            _name = sys.intern(values[2])
        except IndexError:
            _name = None

        try:
            _jip = values[3]
        except IndexError:
            _jip = None

        try:
            _unknown_number = int(values[4])
        except (IndexError, ValueError):
            _unknown_number = None

        try:
            _owner = int(values[5])
        except (IndexError, ValueError):
            _owner = None

        return cls(direct_play_id=_direct_play_id,
                   uid=_uid,
                   name=_name,
                   jip=_jip,
                   unknown_number=_unknown_number,
                   owner=_owner)


@total_ordering
class ConnectionEntry:
    """
    Representation of a single Connection or disconnection event.

    Holds optional data about the log-file also.

    Should only be instantiated through the helper classmethod `from_dict`!
    """

    __slots__ = ["_connection_type",
                 "_steamid",
                 "_name",
                 "_recorded_at",
                 "_server",
                 "_game_map",
                 "_log_file",
                 "_campaign_id",
                 "_antistasi_version",
                 "_mods",
                 "_array_data"]

    def __init__(self,
                 connection_type: ConnectionType,
                 steamid: str,
                 name: str,
                 recorded_at: datetime.datetime,
                 server: Server,
                 game_map: GameMap,
                 log_file: LogFile,
                 campaign_id: CampaignId,
                 antistasi_version: AntistasiVersion,
                 mods: ModList = None,
                 array_data: tuple[float, str, str, bool, int, str] = None) -> None:

        self._connection_type: ConnectionType = connection_type
        self._steamid: str = steamid
        self._name: str = name
        self._recorded_at: datetime.datetime = recorded_at
        self._server: str = server
        self._game_map: str = game_map
        self._log_file: str = log_file
        self._campaign_id: str = campaign_id
        self._antistasi_version: str = antistasi_version
        self._mods: ModList = mods
        self._array_data: ArrayData = ArrayData.new_array_data(*(array_data or tuple()))

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @property
    def steamid(self) -> str:
        return self._steamid

    @property
    def steam_id(self) -> str:
        return self._steamid

    @property
    def name(self) -> str:
        return self._name

    @property
    def recorded_at(self) -> datetime.datetime:
        return self._recorded_at

    @property
    def server(self) -> str:
        return self._server

    @property
    def game_map(self) -> str:
        return self._game_map

    @property
    def log_file(self) -> str:
        return self._log_file

    @property
    def campaign_id(self) -> str:
        return self._campaign_id

    @property
    def antistasi_version(self) -> str:
        return self._antistasi_version

    @property
    def mods(self) -> frozenset[str]:
        return self._mods

    @property
    def array_data(self) -> tuple[float, str, str, bool, int, str]:
        return self._array_data

    @classmethod
    def _recorded_at_converter(cls, in_value: Union[str, int, float, datetime.datetime]) -> datetime.datetime:
        """
        Converts the value to an datetime in UTC if possible.

        Is able to handle input as string(isoformat), number(timestamp) or datetime object directly.

        Args:
            in_value (Union[str, int, float, datetime.datetime]): raw value to be converted.

        Raises:
            ValueError: raised if the value is not an isoformat string, a timestamp number or a datetime object

        Returns:
            datetime.datetime: aware datetime object in UTC-timezone.
        """
        if isinstance(in_value, datetime.datetime):
            return in_value.astimezone(tz=datetime.timezone.utc)

        try:
            in_value = float(in_value)
        except TypeError:
            pass

        if isinstance(in_value, str):
            return datetime.datetime.fromisoformat(in_value).astimezone(tz=datetime.timezone.utc)

        if isinstance(in_value, (int, float)):
            return datetime.datetime.fromtimestamp(in_value, tz=datetime.timezone.utc)

        raise ValueError(f"Value for 'recorded_at' of {cls.__name__!r} has to be either a timestamp, an isoformat-datetime string or a datetime object, not {type(in_value)!r}.")

    @classmethod
    def from_dict(cls, in_dict: Mapping[str, object], cache: AuxCache = None) -> "ConnectionEntry":
        try:
            raw_recorded_at = in_dict["recorded_at"]
        except KeyError:
            raw_recorded_at = in_dict["timestamp"]

        try:
            array_data = in_dict["player_array_data"]

        except KeyError:
            array_data = in_dict["array_data"]

        return cls(connection_type=ConnectionType(in_dict["connection_type"]),
                   steamid=in_dict["player_id"],
                   name=in_dict["player_name"],
                   recorded_at=cls._recorded_at_converter(raw_recorded_at),
                   server=Server.get_or_create(in_dict.get("server", None), cache=cache),
                   game_map=GameMap.get_or_create(in_dict.get("game_map", None), cache=cache),
                   log_file=LogFile.get_or_create(in_dict.get("log_file", None), cache=cache),
                   campaign_id=CampaignId.get_or_create(in_dict.get("campaign_id", None), cache=cache),
                   antistasi_version=AntistasiVersion.get_or_create(in_dict.get("antistasi_version", None), cache=cache),
                   mods=ModList.get_or_create([Mod.get_or_create(i, cache=cache) for i in in_dict.get("mods", [])], cache=cache),
                   array_data=tuple(array_data))

    @ property
    def direct_play_id(self) -> Optional[int]:
        try:
            return int(self.array_data[0])
        except IndexError:
            return None

    def __lt__(self, other: object) -> bool:
        if isinstance(other, ConnectionEntry):
            return self.recorded_at < other.recorded_at

        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConnectionEntry):
            return (self._recorded_at,
                    self._steamid,
                    self._connection_type,
                    self._name,
                    self._log_file,
                    self._server,
                    self._game_map,
                    self._campaign_id,
                    self._antistasi_version) == (other._recorded_at,
                                                 other._steamid,
                                                 other._connection_type,
                                                 other._name,
                                                 other._log_file,
                                                 other._server,
                                                 other._game_map,
                                                 other._campaign_id,
                                                 other._antistasi_version)

        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(steamid={self._steamid!r} ,connection_type={self._connection_type!r}, name={self._name!r}, recorded_at={self._recorded_at!r}, server={self._server!r}, log_file={self._log_file!r}, game_map={self._game_map!r}, campaign_id={self._campaign_id!r})"

    def __hash__(self) -> int:
        return hash((self._recorded_at,
                     self._steamid,
                     self._connection_type,
                     self._name,
                     self._log_file,
                     self._server,
                     self._game_map,
                     self._campaign_id,
                     self._antistasi_version))

    def __rich_console__(self,
                         console: "Console",
                         options: "ConsoleOptions") -> "RenderResult":

        data = {}
        for attr_name in ("steam_id", "name", "connection_type", "recorded_at", "server", "log_file", "game_map", "campaign_id", "antistasi_version", "mods", "array_data"):
            data[attr_name] = getattr(self, attr_name)

        yield make_renderable_simple_dict(data, title=self.__class__.__name__)
# region [Main_Exec]


if __name__ == '__main__':
    pass
# endregion [Main_Exec]

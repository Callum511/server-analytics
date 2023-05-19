"""
WiP.

Soon.
"""

# region [Imports]


import datetime
from typing import Any, Union, Optional, Generator, TypedDict, Mapping, Protocol, runtime_checkable, TextIO, BinaryIO, TYPE_CHECKING
from pathlib import Path
import dataclasses
import enum


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


@enum.unique
class ConnectionType(enum.Enum):
    NO_TYPE = enum.auto()

    CONNECTED = enum.auto()
    CONNECTING = enum.auto()

    DISCONNECTED = enum.auto()
    DISCONNECTING = enum.auto()

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if value is None:
            return cls.NO_TYPE

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


@dataclasses.dataclass(frozen=True, slots=True)
class ConnectionEntry:
    connection_type: ConnectionType = dataclasses.field(hash=True)
    steamid: str = dataclasses.field(hash=True)
    name: str = dataclasses.field(hash=True)
    recorded_at: datetime.datetime = dataclasses.field(hash=True)
    server: str = dataclasses.field(hash=True)
    game_map: str = dataclasses.field(hash=True)
    log_file: str = dataclasses.field(hash=True)
    campaign_id: str = dataclasses.field(hash=True)
    antistasi_version: str = dataclasses.field(hash=True)
    mods: frozenset[str] = dataclasses.field(default=frozenset(), hash=True, repr=False)
    array_data: tuple[float, str, str, bool, int, str] = dataclasses.field(default=tuple(), hash=False, repr=False)

    @classmethod
    def _recorded_at_converter(cls, in_value: Union[str, int, float, datetime.datetime]) -> "ConnectionEntry":
        if isinstance(in_value, datetime.datetime):
            return in_value.astimezone(tz=datetime.timezone.utc)

        if isinstance(in_value, str):
            return datetime.datetime.fromisoformat(in_value)

        if isinstance(in_value, (int, float)):
            return datetime.datetime.fromtimestamp(in_value, tz=datetime.timezone.utc)

        raise ValueError(f"Value for 'recorded_at' of {cls.__name__!r} has to be either a timestamp, an isoformat-datetime string or a datetime object, not {type(in_value)!r}.")

    @classmethod
    def from_dict(cls, in_dict: Mapping[str, object]) -> "ConnectionEntry":

        return cls(connection_type=ConnectionType(in_dict.get("connection_type", None)),
                   steamid=in_dict["player_id"],
                   name=in_dict["player_name"],
                   recorded_at=cls._recorded_at_converter(in_dict["recorded_at"]),
                   server=in_dict.get("server", None),
                   game_map=in_dict.get("game_map", None),
                   log_file=in_dict.get("log_file", None),
                   campaign_id=in_dict.get("campaign_id", None),
                   antistasi_version=in_dict.get("antistasi_version", None),
                   mods=frozenset(in_dict.get("mods", [])),
                   array_data=tuple(in_dict.get("array_data", [])))


# region [Main_Exec]
if __name__ == '__main__':
    ...
# endregion [Main_Exec]

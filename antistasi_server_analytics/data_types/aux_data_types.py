"""
WiP.

Soon.
"""

# region [Imports]

import os
import re
import sys
import json
import queue
import math
import base64
import pickle
import random
import shelve
import dataclasses
import shutil
import asyncio
import logging
import sqlite3
import platform

import subprocess
import inspect

from time import sleep, process_time, process_time_ns, perf_counter, perf_counter_ns
from io import BytesIO, StringIO
from abc import ABC, ABCMeta, abstractmethod
from copy import copy, deepcopy
from enum import Enum, Flag, auto, unique
from pprint import pprint, pformat
from pathlib import Path
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)
from zipfile import ZipFile, ZIP_LZMA
from datetime import datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering, cached_property, cache
from contextlib import contextmanager, asynccontextmanager, nullcontext, closing, ExitStack, suppress
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, wait, as_completed, ALL_COMPLETED, FIRST_EXCEPTION, FIRST_COMPLETED
from weakref import WeakValueDictionary
from rich.pretty import Pretty
from rich.protocol import rich_cast
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from threading import RLock, Lock
if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


T_CACHED_TYPE = TypeVar("T_CACHED_TYPE", bound="BaseAuxItem")


class AuxCache:
    __slots__ = ("_data",
                 "data_lock")

    def __init__(self) -> None:
        self._data: dict[WeakValueDictionary[str, "BaseAuxItem"]] = {}
        self.data_lock = Lock()

    def get_all_instances(self, typus: type[T_CACHED_TYPE]) -> tuple[T_CACHED_TYPE]:

        if typus not in self._data:
            self._data[typus] = WeakValueDictionary()
            return tuple()

        return tuple(self._data[typus].values())

    def get_instance(self,
                     typus: type[T_CACHED_TYPE],
                     key: object) -> Optional[T_CACHED_TYPE]:

        try:
            return self._data[typus][key]
        except KeyError:
            if typus not in self._data:
                self._data[typus] = WeakValueDictionary()
            return None

    def set_instance(self,
                     typus: type[T_CACHED_TYPE],
                     key: object,
                     value: T_CACHED_TYPE) -> None:

        if typus not in self._data:
            self._data[typus] = WeakValueDictionary()

        self._data[typus][key] = value


class BaseAuxItem:
    __slots__ = ("_name",
                 "__weakref__")

    def __init__(self,
                 name: str) -> None:
        self._name = self._normalize_name(name)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def _normalize_name(cls, name: str) -> str:
        return name.casefold().strip().replace(" ", "_").replace("-", "_")

    @classmethod
    def get_or_create(cls,
                      name: Union[str, None],
                      cache: AuxCache = None) -> Union[Self, None]:

        if name is None:
            return None

        if cache is None:
            return cls(name)
        with cache.data_lock:
            instance = cache.get_instance(typus=cls, key=cls._normalize_name(name))

            if instance is None:
                instance = cls(name)
                cache.set_instance(typus=cls, key=instance.name, value=instance)
        return instance

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name

        if isinstance(other, str):
            return self.name == self._normalize_name(other)

    def __hash__(self) -> int:
        return hash((self._name,))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name!r})'

    def __str__(self) -> str:
        return self.name

    def __rich__(self) -> str:
        return self.name


class Server(BaseAuxItem):
    __slots__ = tuple()


class LogFile(BaseAuxItem):
    __slots__ = tuple()


class GameMap(BaseAuxItem):
    __slots__ = tuple()


class AntistasiVersion(BaseAuxItem):
    __slots__ = tuple()


class CampaignId(BaseAuxItem):
    __slots__ = tuple()


class Server(BaseAuxItem):
    __slots__ = tuple()


class Mod(BaseAuxItem):
    __slots__ = tuple()


class ModList:
    __slots__ = ("_mods",
                 "__weakref__")

    def __init__(self,
                 mods: Iterable[Mod]) -> None:
        self._mods = frozenset(mods)

    @property
    def mods(self) -> frozenset[Mod]:
        return self._mods

    @classmethod
    def get_or_create(cls,
                      mods: Union[Iterable[str], None],
                      cache: AuxCache = None) -> Union[Self, None]:

        if mods is None or len(mods) <= 0:
            return None

        if cache is None:
            return cls(mods)

        mods = frozenset(mods)
        instance = cache.get_instance(typus=cls, key=mods)
        if instance is None:
            instance = cls(mods)
            cache.set_instance(typus=cls, key=instance.mods, value=instance)

        return instance

    def __contains__(self, other: object) -> bool:
        return other in self._mods

    def __hash__(self) -> int:
        return hash((self._mods,))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._mods == other._mods

        if isinstance(other, Iterable):
            return len(self._mods.difference(other)) == 0

        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(mods={self.mods!r})'

    def __str__(self) -> str:
        return str(sorted([str(m) for m in self.mods]))

    def __rich_console__(self,
                         console: "Console",
                         options: "ConsoleOptions") -> "RenderResult":

        yield Pretty(sorted([rich_cast(m) for m in self.mods]))


# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

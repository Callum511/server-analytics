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
from antistasi_server_analytics.commands.base_command import command_wrapper

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from antistasi_server_analytics.data_types.connection_entry import ConnectionType, ConnectionEntry
if TYPE_CHECKING:
    from antistasi_server_analytics.application_context import ApplicationContext


# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


@command_wrapper(categories=("amount", "info"))
def amount_data(context: "ApplicationContext"):
    players = context.data
    return players.amount_all_connections


@command_wrapper(categories=("info", "latest", "connection_info"))
def latest_connection(context: "ApplicationContext"):
    players = context.data
    connection = players.all_connections[-1]

    return connection


@command_wrapper(categories=("info", "latest", "player_info"))
def latest_connection_player(context: "ApplicationContext"):
    players = context.data

    connection: ConnectionEntry = [c for c in players.all_connections if c.connection_type is ConnectionType.CONNECTED][-1]

    player = players.get(connection.steam_id)

    return player


@command_wrapper(categories=("info", "most", "player_info"))
def most_connected_player(context: "ApplicationContext"):
    players = context.data
    most_connected = sorted(players.players, key=lambda x: x.amount_connections)[-1]

    return most_connected


@command_wrapper(categories=("info", "most", "player_info"))
def most_disconnected_player(context: "ApplicationContext"):
    players = context.data
    most_disconnected = sorted(players.players, key=lambda x: x.amount_disconnections)[-1]

    return most_disconnected


@command_wrapper(categories=("info", "newest", "player_info"))
def newest_player(context: "ApplicationContext"):
    players = context.data
    all_connections: list[ConnectionEntry] = [c for c in players.all_connections if c.connection_type is ConnectionType.CONNECTED]

    cur_idx = 1

    connection: ConnectionEntry = all_connections[-cur_idx]

    player = players.get(connection.steam_id)

    while True:
        if player.amount_connections == 1:
            break

        cur_idx += 1
        connection = all_connections[-cur_idx]
        player = players.get(connection.steam_id)

    return player


@command_wrapper(categories=("info", "oldest", "player_info"))
def oldest_player(context: "ApplicationContext"):
    players = context.data
    all_connections: list[ConnectionEntry] = [c for c in players.all_connections if c.connection_type is ConnectionType.CONNECTED]

    cur_idx = 1

    connection: ConnectionEntry = all_connections[cur_idx]

    player = players.get(connection.steam_id)

    return player


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

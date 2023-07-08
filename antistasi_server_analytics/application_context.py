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
from typing import (TYPE_CHECKING, Mapping, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
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
from threading import Lock, RLock
from operator import add
from rich.style import StyleType

from rich.text import Text
from rich.box import HEAVY, HEAVY_EDGE, HEAVY_HEAD, DOUBLE, DOUBLE_EDGE, ROUNDED
from rich.protocol import is_renderable
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from rich.theme import Theme
from rich.scope import render_scope
from antistasi_server_analytics.data_types.player_data_container import PlayerDataContainer
from sortedcontainers import SortedDict, SortedList, SortedSet
from rich.console import Console as RichConsole, RenderableType, Group
from rich.panel import Panel
from rich.style import Style
from rich.progress import Progress, Task, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn, TotalFileSizeColumn, MofNCompleteColumn, ProgressColumn
from types import MappingProxyType
from antistasi_server_analytics.misc.output_helper import make_renderable_simple_dict
from antistasi_server_analytics.loader import LOADER_CONTAINER, LoaderContainer
if TYPE_CHECKING:
    from antistasi_server_analytics.loader._base_loader import BaseLoader
    from antistasi_server_analytics.commands.base_command import Command

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class WindowsSafeTheme(Theme):

    def __init__(self):
        overwrite_styles = {"scope.key": Style(color="yellow", italic=False),
                            "scope.key.special": Style(color="yellow", italic=False, dim=True), }
        super().__init__(overwrite_styles, inherit=True)


def _loader_sort_key(loader_class) -> int:
    return - inspect.getattr_static(loader_class, "specificity", 1)


class ItemDigitalProgressColumn(MofNCompleteColumn):
    def render(self, task: Task) -> Text:
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        total_width = len(str(total))
        return Text(
            f"{completed:{total_width}d}{self.separator}{total}",
            style="progress.download",
            justify="right"

        )


def _progress_bar_columns() -> tuple[ProgressColumn]:
    return (TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            ItemDigitalProgressColumn())


DEFAULT_CONFIGURATION: dict[str, object] = {"now_time": "LAST_ENTRY"}


class ApplicationContext:
    loader_collection: LoaderContainer = LOADER_CONTAINER
    __slots__ = ("__weakref__",

                 "_is_setup",
                 "_console",
                 "_sources",
                 "_player_data_container",
                 "_to_run_commands",
                 "_configuration")

    def __init__(self) -> None:
        self._is_setup: bool = False
        self._console: RichConsole = None
        self._sources: tuple["BaseLoader"] = None
        self._player_data_container: PlayerDataContainer = None
        self._to_run_commands: set["Command"] = set()

        self._configuration: dict[str, object] = DEFAULT_CONFIGURATION

    def add_to_run_command(self, command: "Command") -> Self:
        self._to_run_commands.add(command)

        return self

    def add_configuration_value(self, name: str, value: object) -> Self:
        self._configuration[name] = value
        return self

    def add_configuration(self, configuration: dict[str, object] = None) -> None:
        self._configuration = self._configuration | (configuration or {})
        return self

    def _setup_console(self) -> None:
        self._console = RichConsole(soft_wrap=True, theme=WindowsSafeTheme())
        self._console.rule()

    def _setup_player_data_container(self) -> None:
        self._player_data_container = PlayerDataContainer(now_time=self.configuration["now_time"])

    def _setup_fill_player_data_container(self) -> None:
        with Progress(*_progress_bar_columns(), console=self.console, expand=True, transient=True) as progress_bar:
            resolved_loaders = []
            for source in self._sources:
                resolved_loaders += source.get_resolved_loaders()

            loader_task_id = progress_bar.add_task("Loading from Loaders...", total=len(resolved_loaders))
            sub_task_id = progress_bar.add_task("Loading data from provided source...")

            for source in resolved_loaders:
                source.add_to_player_container(self._player_data_container, progress_bar=progress_bar, progress_task_id=sub_task_id)
                progress_bar.advance(loader_task_id)

    def _setup_fill_player_data_container_concurrently(self) -> None:

        def _actual_adding(in_source: "BaseLoader"):
            in_source.add_to_player_container(self._player_data_container)

        with ThreadPoolExecutor() as pool:
            with Progress(*_progress_bar_columns(), console=self.console, expand=True, transient=True) as progress_bar:
                resolved_loaders = []
                for source in self._sources:
                    resolved_loaders += source.get_resolved_loaders()

                resolved_loaders = sorted(resolved_loaders, key=lambda x: x.concurrent_priority)

                loader_task_id = progress_bar.add_task("Loading from Loaders...", total=len(resolved_loaders))
                tasks = []
                for source in resolved_loaders:
                    task = pool.submit(_actual_adding, source)
                    task.add_done_callback(lambda x: progress_bar.advance(loader_task_id))
                    tasks.append(task)

                done, not_done = wait(tasks, return_when=ALL_COMPLETED)
                for d in done.union(not_done):
                    if d.exception():
                        raise d.exception()

    def setup(self) -> Self:
        if self._is_setup is True:
            raise RuntimeError(f"{self.__class__.__name__!r} is already setup.")

        # self._setup_console()
        self._setup_player_data_container()
        start_time = perf_counter()
        self._setup_fill_player_data_container()
        # self._setup_fill_player_data_container_concurrently()
        end_time = perf_counter()
        self.console.print(f"[bold] loading data took[/bold] [u]{round(end_time-start_time, ndigits=2)!r} s[/u]")
        self._is_setup = True
        return self

    @property
    def print(self):
        return self.console.print

    @property
    def data(self) -> PlayerDataContainer:
        return self._player_data_container

    @property
    def console(self) -> RichConsole:
        if self._console is None:
            self._setup_console()
        return self._console

    @property
    def configuration(self) -> MappingProxyType[dict[str, object]]:
        return MappingProxyType(self._configuration)

    @property
    def sorted_commands(self) -> tuple["Command"]:
        _modified_commands = sorted(self._to_run_commands, key=lambda x: x.name)

        return tuple(_modified_commands)

    def _convert_sub_result(self, sub_result: object) -> RenderableType:
        if isinstance(sub_result, (tuple, list, set, frozenset)):
            sub_result = Group(*[self._convert_sub_result(i) for i in sub_result])
        if not is_renderable(sub_result):
            if isinstance(sub_result, Mapping):
                sub_result = make_renderable_simple_dict(sub_result)

            else:
                sub_result = str(sub_result)
        return sub_result

    def print_result(self, command: "Command", result: object) -> None:
        result = self._convert_sub_result(result)

        self.console.print(Panel.fit(result,
                                     title=f"[b u dark_sea_green]COMMAND:[/b u dark_sea_green] [bold bright_white]{command.pretty_name}[/bold bright_white]",
                                     title_align="left",
                                     style="on grey11",
                                     border_style="bright_white",
                                     box=ROUNDED))

    def run(self) -> None:
        for cmd in self.sorted_commands:
            result = cmd(self)
            self.print_result(cmd, result)
            self.console.print("")

        # region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

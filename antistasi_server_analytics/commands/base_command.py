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
from typing import (TYPE_CHECKING, Iterable, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)
from collections import Counter, ChainMap, deque, namedtuple, defaultdict

from zipfile import ZipFile, ZIP_LZMA
from datetime import datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering, cached_property, cache
from contextlib import contextmanager, asynccontextmanager, nullcontext, closing, ExitStack, suppress
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, wait, as_completed, ALL_COMPLETED, FIRST_EXCEPTION, FIRST_COMPLETED


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

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


COMMAND_TYPE = Callable[["ApplicationContext"], None]


def _make_name(in_func: COMMAND_TYPE) -> str:
    return in_func.__name__.casefold()


def _make_pretty_name(in_func: COMMAND_TYPE) -> str:
    raw_name = getattr(in_func, "name", in_func.__name__)

    return raw_name.replace("_", " ").title()


def _make_cli_name(in_func: COMMAND_TYPE) -> str:
    raw_name = getattr(in_func, "name", in_func.__name__)
    return raw_name.replace("_", "-").casefold()


class Command:
    __slots__ = ("command_function",
                 "_name",
                 "pretty_name",
                 "cli_name",
                 "disabled",
                 "categories",
                 "description")

    _is_command: bool = True

    def __init__(self,
                 command_function: COMMAND_TYPE,
                 name: str = None,
                 pretty_name: str = None,
                 cli_name: str = None,
                 categories: Iterable[str] = None,
                 description: str = None,
                 disabled: bool = False) -> None:
        self.command_function = command_function
        self._name = name or self._make_default_command_name()
        self.pretty_name = pretty_name or self._make_default_pretty_name()
        self.cli_name = cli_name or self._make_default_cli_name()
        self.disabled = disabled
        self.categories = self._make_categories(categories)
        self.description = description or self._make_default_description()

    @property
    def name(self) -> str:
        return self._name

    def _make_default_description(self) -> str:
        return inspect.getdoc(self.command_function) or "No description"

    def _make_categories(self, in_categories: Iterable[str] = None) -> frozenset[str]:

        def _normalize_category_part(in_part: str) -> str:
            _part = in_part.strip().casefold().removeprefix("_").removesuffix("_commands").removesuffix("_command")

            return _part.upper()

        in_categories = in_categories or self.command_function.__module__.rsplit(".", 1)[-1:]
        category_parts = [_normalize_category_part(part) for part in in_categories]

        return frozenset(category_parts)

    def _make_default_command_name(self) -> str:
        return self.command_function.__name__.casefold()

    def _make_default_pretty_name(self) -> str:
        return self.name.replace("_", " ").title()

    def _make_default_cli_name(self) -> str:
        return self.name.replace("_", "-").casefold()

    def __call__(self,
                 context: "ApplicationContext") -> object:
        return self.command_function(context)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name!r}, categories={sorted(self.categories)!r})'


# def command_wrapper(name: str = None,
#                     pretty_name: str = None,
#                     cli_name: str = None,
#                     disabled: bool = False):
#         in_func.name = name or _make_name(in_func)
#         in_func.cli_name = cli_name or _make_cli_name(in_func)
#         in_func.pretty_name = pretty_name or _make_pretty_name(in_func)
#         in_func.disabled = disabled
#         in_func.is_command = True
#         return in_func

#     return _modify_func


def command_wrapper(name: str = None,
                    pretty_name: str = None,
                    cli_name: str = None,
                    categories: Iterable[str] = None,
                    disabled: bool = False,
                    description: str = None):

    def _inner(in_func: COMMAND_TYPE) -> Command:
        return Command(command_function=in_func,
                       name=name,
                       pretty_name=pretty_name,
                       cli_name=cli_name,
                       categories=categories,
                       disabled=disabled,
                       description=description)

    return _inner


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

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


import argparse
from rich.console import Console as RichConsole, RenderableType
from rich.panel import Panel
from rich.terminal_theme import MONOKAI, NIGHT_OWLISH
from rich.style import Style
from rich.box import Box, HEAVY, HEAVY_EDGE, HEAVY_HEAD, HORIZONTALS, SIMPLE, SIMPLE_HEAVY, SQUARE, ROUNDED, MINIMAL, DOUBLE_EDGE


from antistasi_server_analytics import __version__

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if TYPE_CHECKING:
    ...

# endregion [Imports]


# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


IS_IGNORED: TypeAlias = object


class BaseParser(argparse.ArgumentParser):

    def __init__(self,
                 prog: Optional[str] = None,
                 usage: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None,
                 parents: Sequence[argparse.ArgumentParser] = None,
                 prefix_chars: str = "-",
                 fromfile_prefix_chars: Optional[str] = None,
                 argument_default: object = None,
                 conflict_handler: str = "error",
                 add_help: bool = True,
                 allow_abbrev: bool = True,
                 exit_on_error: bool = True) -> None:

        super().__init__(prog=prog,
                         usage=usage,
                         description=description,
                         epilog=epilog,
                         parents=parents or [],
                         formatter_class=argparse.HelpFormatter,
                         prefix_chars=prefix_chars,
                         fromfile_prefix_chars=fromfile_prefix_chars,
                         argument_default=argument_default,
                         conflict_handler=conflict_handler,
                         add_help=add_help,
                         allow_abbrev=allow_abbrev,
                         exit_on_error=exit_on_error)

        self.add_argument('--version', "-V", action='version', version=__version__)


# region [Main_Exec]
if __name__ == '__main__':
    pass
# endregion [Main_Exec]

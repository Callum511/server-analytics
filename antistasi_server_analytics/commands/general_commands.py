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
from rich.panel import Panel
from rich.tree import Tree
from rich.scope import render_scope
from antistasi_server_analytics.misc.output_helper import make_renderable_simple_dict
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


from antistasi_server_analytics.application_context import ApplicationContext
# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


@command_wrapper(categories=("General", ))
def general_data(context: ApplicationContext):
    players = context.data
    time_data = sorted((i.recorded_at for i in players.all_connections))
    results = {"Amount Connections": players.amount_all_connections,
               "Average connections": players.average_amount_connections(),
               "Mode connections": players.mode_amount_connections(),
               "Multimode connections": players.multimode_amount_connections(),
               "Median connections": players.median_amount_connections(),
               "Unique players (all time)": players.amount_unique_all_time(),
               "New players (30 days)": len(players.new30d()),
               "Stdev connections": players.stdev_amount_connections(),
               "Quantiles connections": players.quantiles_amount_connections(),
               "time_frame": (str(time_data[0]), str(time_data[-1]), str(time_data[-1] - time_data[0]))}

    return results


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

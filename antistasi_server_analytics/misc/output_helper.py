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
from itertools import cycle
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.style import StyleType
from rich.tree import Tree
from rich.table import Table
from rich.box import DOUBLE, DOUBLE_EDGE, HEAVY, ROUNDED, Box
from rich.text import Text, TextType
from rich.protocol import is_renderable, rich_cast
from rich.scope import render_scope
from rich.align import Align, AlignMethod
from rich.console import Group, RenderableType
from rich.pretty import Pretty
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if TYPE_CHECKING:
    from rich.console import RenderableType

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


def _convert_value(in_value: object):
    if is_renderable(in_value):
        return in_value

    if isinstance(in_value, (str, int, float)):
        return in_value

    if in_value is None:
        return in_value

    if isinstance(in_value, Enum):
        return in_value

    if isinstance(in_value, dict):
        return make_renderable_simple_dict(in_value)

    if isinstance(in_value, (list, tuple, set, frozenset)):
        return [_convert_value(i) for i in in_value]

    return str(in_value)


def make_renderable_simple_dict(in_dict: dict[str, object],
                                *,
                                title: Optional[str] = None) -> "RenderableType":
    actual_dict = {}
    for key, value in in_dict.items():
        value = _convert_value(value)

        actual_dict[key] = value

    return render_scope(actual_dict, sort_keys=False, title=title)


class ResultPanel(Panel):

    def __init__(self,
                 renderable: RenderableType,
                 box: Box = ...,
                 *,
                 title: TextType | None = None,
                 title_align: AlignMethod = "center",
                 subtitle: TextType | None = None,
                 subtitle_align: AlignMethod = "center",
                 safe_box: bool | None = None,
                 expand: bool = True,
                 style: StyleType = "none",
                 border_style: StyleType = "none",
                 width: int | None = None,
                 height: int | None = None,
                 padding: PaddingDimensions = ...,
                 highlight: bool = False) -> None:
        super().__init__(renderable, box, title=title, title_align=title_align, subtitle=subtitle, subtitle_align=subtitle_align, safe_box=safe_box, expand=expand, style=style, border_style=border_style, width=width, height=height, padding=padding, highlight=highlight)


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]

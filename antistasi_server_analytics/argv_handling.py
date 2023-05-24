"""
WiP.

Soon.
"""

# region [Imports]


import sys


from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)

import argparse


from antistasi_server_analytics import __app_name__, __app_pretty_name__, __version__
from antistasi_server_analytics.loader import LOADER_CONTAINER
if TYPE_CHECKING:
    ...

# endregion [Imports]


# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]

# TODO: Maybe a different way of handling cli arguments, maybe rewrite the argparser or use a different package


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

        self.add_argument("sources", nargs="+")

    def parse_args(self, args=None, namespace=None):
        args_namespace = super().parse_args(args=args, namespace=namespace)
        args_namespace.sources = [LOADER_CONTAINER.create_loader(i) for i in args_namespace.sources]
        return args_namespace
# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

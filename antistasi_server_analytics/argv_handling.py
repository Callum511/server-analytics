"""
WiP.

Soon.
"""

# region [Imports]


from argparse import Action, ArgumentParser, Namespace
import sys


from pathlib import Path

from typing import (TYPE_CHECKING, TypeVar, TypeGuard, TypeAlias, Final, TypedDict, Generic, Union, Optional, ForwardRef, final, Callable,
                    no_type_check, no_type_check_decorator, overload, get_type_hints, cast, Protocol, runtime_checkable, NoReturn, NewType, Literal, AnyStr, IO, BinaryIO, TextIO, Any)

from collections.abc import (AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, ByteString, Callable, Collection, Container, Coroutine, Generator,
                             Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, MappingView, MutableMapping, MutableSequence, MutableSet, Reversible, Sequence, Set, Sized, ValuesView)
from collections import defaultdict, ChainMap
import argparse
from itertools import chain

from antistasi_server_analytics import __app_name__, __app_pretty_name__, __version__
from antistasi_server_analytics.loader import LOADER_CONTAINER
from antistasi_server_analytics.commands import COMMAND_BLUEPRINT, COMMAND_EXAMPLE

from rich.syntax import Syntax
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
if TYPE_CHECKING:
    from antistasi_server_analytics.application_context import ApplicationContext
    from antistasi_server_analytics.commands.base_command import Command

# endregion [Imports]


# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]

# TODO: Maybe a different way of handling cli arguments, maybe rewrite the argparser or use a different package


T_ApplicationContext = TypeVar("T_ApplicationContext", bound="ApplicationContext")


class _ListCommandsAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help="List all available commands and exit"):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):

        formatter = parser._get_formatter()
        parser._print_message("Available commands:\n\n")

        table = Table("Name", "Categories", "Description")
        for commands in parser.command_map.values():
            table.add_row(f"[bold]{commands[0].cli_name}[/bold]", ', '.join(f"[u]{cat}[/u]" for cat in sorted(commands[0].categories)), f"[italic]{commands[0].description}[/italic]")

        category_tree = Tree("Categories")
        for cat, commands in parser.command_category_map.items():
            sub_cat_tree = category_tree.add(cat.upper())
            for command in commands:
                sub_cat_tree.add(command.cli_name)
        parser.application_context.console.print(Panel(table, title="Available Commands"))
        parser.application_context.console.print(category_tree)
        parser._print_message(formatter.format_help())
        parser.exit()


class _ShowCommandExampleAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help="Shows an example of how a command function should look like"):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):

        formatter = parser._get_formatter()
        parser.application_context.console.rule("EXAMPLE")
        parser.application_context.console.print(Syntax("\n" + COMMAND_EXAMPLE + "\n", "python", line_numbers=False, background_color="black", highlight_lines={8, 9, 10, 11}))
        parser.application_context.console.rule()
        parser._print_message(formatter.format_help())
        parser.exit()


class _AddCommandAction(argparse.Action):

    def __call__(self,
                 parser: "BaseParser",
                 namespace: Namespace,
                 values: Union[str, Sequence[Any], None],
                 option_string: Optional[str] = None) -> None:
        command_list = getattr(namespace, self.dest, [])
        if command_list is None:
            command_list = []

        try:
            to_add_commands = ChainMap(parser.command_map, parser.command_category_map)[values.casefold()]

        except KeyError:
            raise ValueError(f"No command or category called {values!r}.")

        for command in to_add_commands:
            if command not in command_list:
                command_list.append(command)

        setattr(namespace, self.dest, command_list)


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
        self.application_context = None
        self.add_argument('--version', "-V", action='version', version=__version__)
        self.add_argument("--example", "-e", action=_ShowCommandExampleAction)
        self.add_argument("sources", nargs="+")

        self.command_map: dict[str, "Command"] = {}
        self.command_category_map: defaultdict[str, list["Command"]] = defaultdict(list)
        self.add_commands()

    def _check_value(self, action: Action, value: Any) -> None:
        if isinstance(action, _AddCommandAction):
            if action.choices is not None and value.casefold() not in action.choices:
                return super()._check_value(action, value)
        else:
            return super()._check_value(action, value)

    def add_commands(self) -> None:
        from antistasi_server_analytics.commands import get_all_commands

        for command in get_all_commands():
            self.command_map[command.cli_name.casefold()] = [command]
            for category in command.categories:
                self.command_category_map[category.casefold()].append(command)
        self.add_argument("--command", "-c", action=_AddCommandAction, dest="command_names", metavar="COMMAND_NAME_or_CATEGORY_NAME", choices=list(self.command_map) + list(self.command_category_map))

        self.add_argument("--list-commands", "-l", action=_ListCommandsAction)

    def parse_args(self, application_context: T_ApplicationContext, args=None) -> T_ApplicationContext:

        self.application_context = application_context
        args_namespace = super().parse_args(args=args, namespace=None)

        application_context._sources = [LOADER_CONTAINER.create_loader(i) for i in args_namespace.sources]
        if not getattr(args_namespace, "command_names", []):
            args_namespace.command_names = ["general-data"]
        for command in args_namespace.command_names:
            application_context.add_to_run_command(command)
        return application_context

# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]

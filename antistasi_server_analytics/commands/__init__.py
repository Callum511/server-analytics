
import inspect
from pathlib import Path
from functools import wraps
import pkgutil
from traceback import print_tb
import sys
import importlib
from types import ModuleType
from typing import TYPE_CHECKING, Generator
if TYPE_CHECKING:
    from .base_command import Command


def _extract_commands_from_module(name: str) -> Generator["Command", None, None]:

    def _predicate(in_object: object) -> bool:
        return getattr(in_object, "_is_command", False) is True and in_object.disabled is False

    module = importlib.import_module(name)
    for command_func_name, command_object in inspect.getmembers(module, predicate=_predicate):

        yield command_object


def _import_commands_from_folder() -> tuple["Command"]:

    all_commands = []

    for sub_module in pkgutil.walk_packages(__path__, __name__ + '.', onerror=print_tb):
        for _command in _extract_commands_from_module(sub_module.name):

            all_commands.append(_command)

    return tuple(sorted(all_commands, key=lambda x: x.name))


def _get_all_commands():
    _ALL_COMMANDS: tuple["Command"] = None

    def _inner() -> tuple["Command"]:
        nonlocal _ALL_COMMANDS
        if _ALL_COMMANDS is None:

            _ALL_COMMANDS = _import_commands_from_folder()

        return _ALL_COMMANDS

    return _inner


get_all_commands = _get_all_commands()

COMMAND_BLUEPRINT: str = """

from typing import TYPE_CHECKING

from antistasi_server_analytics.commands.base_command import command_wrapper

if TYPE_CHECKING:
    from antistasi_server_analytics.application_context import ApplicationContext



@command_wrapper()
def {command_name}(context: "ApplicationContext"):
    players = context.data
    ...

""".strip()


COMMAND_EXAMPLE: str = """

from typing import TYPE_CHECKING

from antistasi_server_analytics.commands.base_command import command_wrapper

if TYPE_CHECKING:
    from antistasi_server_analytics.application_context import ApplicationContext


@command_wrapper(categories=("info", "latest"))
def latest_connection(context: "ApplicationContext"):
    connection = sorted(context.data.all_connections, key=lambda x: x.recorded_at)[-1]

    return connection

""".strip()

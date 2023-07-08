import sys
from typing import Union
from antistasi_server_analytics.data_types import PlayerDataContainer, ConnectionType
from antistasi_server_analytics.argv_handling import BaseParser
from rich.console import Console as RichConsole, CONSOLE_HTML_FORMAT, CONSOLE_SVG_FORMAT, Group
from rich.panel import Panel
from rich.table import Table
from rich.box import HEAVY, HEAVY_EDGE, HEAVY_HEAD, ROUNDED, SIMPLE, SQUARE_DOUBLE_HEAD
from rich.align import Align
from rich.progress import Progress
from rich.progress import track
from time import sleep
from concurrent.futures import ThreadPoolExecutor, Future, as_completed, ALL_COMPLETED
from sortedcontainers import SortedList
from antistasi_server_analytics.application_context import ApplicationContext


import pp


def main(arguments: Union[list[str], None] = None):

    application_context = ApplicationContext()

    parser = BaseParser()
    application_context = parser.parse_args(application_context, args=arguments)

    application_context.setup()
    application_context.run()


if __name__ == '__main__':
    main()

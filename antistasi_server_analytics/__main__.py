

from antistasi_server_analytics.data_types import PlayerDataContainer, ConnectionType
from antistasi_server_analytics.argv_handling import BaseParser
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table
from rich.box import HEAVY, HEAVY_EDGE, HEAVY_HEAD, ROUNDED
from rich.align import Align


def main():
    parser = BaseParser()
    parser_result = parser.parse_args()
    xx = PlayerDataContainer()

    for source in parser_result.sources:
        xx = source.add_to_player_container(xx, data_filter=lambda x: x.connection_type is ConnectionType.CONNECTED)

    console = RichConsole(soft_wrap=True)
    console.rule()
    table = Table("Name", "Value",
                  box=ROUNDED,
                  title=f"data from {xx.amount_all_connections} Connections.".title(),
                  header_style="bright_white on chartreuse4",
                  title_style="bold",
                  row_styles=["on grey19", "on grey27"],
                  highlight=True)

    for meth_name in ("amount_unique_all_time", "amount_unique_24h", "amount_unique_7d", "average_amount_connections", "median_amount_connections", "mode_amount_connections", "multimode_amount_connections", "stdev_amount_connections", "quantiles_amount_connections"):
        table.add_row(meth_name.replace("_", " ").title(), Align(str(getattr(xx, meth_name)()), align="right"))

    console.print(table)
    console.rule()


if __name__ == '__main__':
    main()

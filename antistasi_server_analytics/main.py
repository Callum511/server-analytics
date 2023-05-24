import csv
import datetime
from typing import Union, Optional, Generator, TypedDict, Tuple, List
import json
import os
from pathlib import Path


class DataEntry(TypedDict):
    recorded_at: datetime.datetime
    player_id: str
    player_name: str
    player_array_data: Tuple[float, str, str, bool, int, str]
    original_message: str
    log_file: str
    game_map: str
    campaign_id: str
    antistasi_version: str
    mods: Tuple[str]
    server: str


def _load_data_entries_from_file(in_file: Path) -> Generator[DataEntry, None, None]:
    with in_file.open("r", encoding='utf-8', errors='ignore') as f:
        for _item in json.load(f):
            _item["recorded_at"] = datetime.datetime.fromtimestamp(_item["recorded_at"], tz=datetime.timezone.utc)
            _item["player_array_data"] = tuple(_item["player_array_data"])
            _item["mods"] = tuple(_item["mods"])

            yield DataEntry(**_item)


def iter_data_entries(in_folder: os.PathLike, file_prefix: str = "player_data") -> Generator[DataEntry, None, None]:
    for _file in Path(in_folder).resolve().iterdir():
        if _file.is_file() is False:
            continue

        if _file.suffix != ".json":
            continue

        if not _file.name.startswith(file_prefix):
            continue

        yield from _load_data_entries_from_file(in_file=_file)


class Player:
    # slots to make it less memory heavy, saves a lot of memory.
    __slots__ = ("name",
                 "steamid",
                 "connections")

    def __init__(self,
                 name: str,
                 steamid: str) -> None:

        self.name = name
        self.steamid = steamid

        self.connections: List[datetime.datetime] = []

    @property
    def first_connection(self) -> Optional[datetime.datetime]:
        if len(self.connections) == 0:
            return None

        if len(self.connections) == 1:
            return self.connections[0]

        return min(self.connections)

    @property
    def last_connection(self) -> Optional[datetime.datetime]:
        if len(self.connections) == 0:
            return None

        if len(self.connections) == 1:
            return self.connections[0]

        return max(self.connections)

    @property
    def amount_connections(self) -> int:
        return len(self.connections)

    @property
    def seen24h(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=24))

    @property
    def seen7d(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=7))

    @property
    def seen30d(self):
        return self.last_connection > (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=30))

    def add_connection(self, new_connection_time: datetime.datetime) -> None:
        self.connections.append(new_connection_time)
        self.connections = sorted(self.connections)

    def __repr__(self):
        attr = {attr_name: getattr(self, attr_name) for attr_name in (self.__slots__ + ("first_connection", "last_connection"))}

        return ', '.join(f"{name}: {value}" for name, value in attr.items())


class PlayerList:
    __slots__ = ("players",)

    def __init__(self):
        self.players = []

    def add(self, player):
        self.players.append(player)

    def get(self, steamid):
        for player in self.players:
            if player.steamid == steamid:
                return player
        return None

    def get_all(self):
        return self.players

    def get_all_sorted(self, sort_by, reverse=False):
        return sorted(self.players, key=lambda x: getattr(x, sort_by), reverse=reverse)

    def average_connections(self):
        total = 0
        for player in self.players:
            total += player.amount_connections
        return total / len(self.players)

    def mode_connections(self):
        connections = []
        for player in self.players:
            connections.append(player.amount_connections)
        return max(set(connections), key=connections.count)

    def median_connections(self):
        connections = []
        for player in self.players:
            connections.append(player.amount_connections)
        connections.sort()
        if len(connections) % 2 == 0:
            return (connections[int(len(connections) / 2)] + connections[int(len(connections) / 2 - 1)]) / 2
        else:
            return connections[int(len(connections) / 2)]

    def unique_all_time(self):
        steamids = []
        for player in self.players:
            if player.steamid not in steamids:
                steamids.append(player.steamid)
        return len(steamids)

    def unique_24h(self):
        steamids = []
        for player in self.players:
            if player.seen24h and player.steamid not in steamids:
                steamids.append(player.steamid)
        return len(steamids)

    def unique_7d(self):
        steamids = []
        for player in self.players:
            if player.seen7d and player.steamid not in steamids:
                steamids.append(player.steamid)
        return len(steamids)

    # this returns a list of players who have connected for the first time in the last 30 days
    def new30d(self):
        players = []
        for player in self.players:
            if player.seen30d:
                if player.first_connection > datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=30):
                    players.append(player)
        return players


def read_csv(filename):
    # good practice to specify the encoding as a lot of shit can break if you don't (especially on windows).
    # so just add `encoding='utf-8', errors='ignore'`, I have it set as a snippet
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = []
        for row in reader:
            data.append(row)

        return data


def write_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for row in data:
            writer.writerow(row)


def analyse(data):
    # data is a 3 column list of lists
    # [date, steamid, name]
    players = PlayerList()
    data = data[1:]
    for row in data:
        date = row[0]
        steamid = row[1]
        name = row[2]
        player = players.get(steamid) or Player(name=name, steamid=steamid)
        player.add_connection(datetime.datetime.fromtimestamp(date, tz=datetime.timezone.utc))

    return players


def analyse_from_json(folder: os.PathLike, file_prefix: str = "player_data") -> PlayerList:
    players = PlayerList()
    for raw_player_data in iter_data_entries(folder, file_prefix=file_prefix):
        steamid = raw_player_data["player_id"]
        name = raw_player_data["player_name"]
        date = raw_player_data["recorded_at"]
        player = players.get(steamid)
        if player is None:
            player = Player(name=name, steamid=steamid)
            players.add(player)

        player.add_connection(date)
    return players


def main():
    # data = read_csv("player_data.csv")
    # players = analyse(data)
    players = analyse_from_json(folder=r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_Logbook\antistasi_logbook\debug_dump\connection_data_json")
    players_sorted = players.get_all_sorted("connections", True)
    recent_players = []
    frequent_flyers = []
    average_connections = players.average_connections()
    for player in players_sorted:
        if player.seen30d:
            recent_players.append(player)

    # if the player is in the top 10% of connections, add them to the frequent flyers list
    for player in recent_players:
        if player.amount_connections > (average_connections * 1.1):
            frequent_flyers.append(player)

    # sort the frequent flyers by connections
    frequent_flyers_sorted = sorted(frequent_flyers, key=lambda x: x.amount_connections, reverse=True)
    print(f"Average connections: {players.average_connections():.3f}")
    print(f"Mode connections: {players.mode_connections()}")
    print(f"Median connections: {players.median_connections()}")
    print(f"Unique players (all time): {players.unique_all_time():,}")
    print(f"New players (30 days): {len(players.new30d()):,}")
    print(f"Frequent flyers: {len(frequent_flyers_sorted):,}")
    csv_data = [["name", "connections"]]
    for player in frequent_flyers_sorted:
        csv_data.append([player.name, player.amount_connections])

    write_csv("frequent_flyers.csv", csv_data)


# always wrap your main entry point in a `if __name__ == '__main__'` clause, this prevents the main() function to run
# if you ever import that file. also is necessary if you want to use Multiprocessing.
if __name__ == '__main__':

    main()

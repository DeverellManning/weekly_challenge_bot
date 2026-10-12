import tomllib
from typing import Any


def load(conf_path : str) -> dict[str, Any]:
    config = {}
    try:
        with open(conf_path, "rb") as cf:
            config = tomllib.load(cf)
    except FileNotFoundError:
        print("Creating config file...")
        create_config_file(conf_path)
        config = load(conf_path)
    finally:
        return config


def create_config_file(conf_path : str):
    with open(conf_path, "xt") as cf:
        print("", file=cf)


def add_guild(conf_path, guild_id, guild_name):
    a = f"""
# Guild config for "{guild_name}"
[{guild_id}]
disabled = true
role_id = 0 # Replace with role ID for players
channel_id = 0 # Replace with the channel ID you want the bot to work in.
round_start_time = 19:00:00 # When weekly quests are decided and announced. (24 hour time format)
round_start_day = 7 # Monday = 0, Tuesday = 1 ... Sunday = 7
round_end_time = 16:00:00
round_end_day = 6"""

    with open(conf_path, "at") as cf:
        print(a, file=cf)
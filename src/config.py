import json
from dataclasses import dataclass


@dataclass
class Config:
    svg_path: str
    svg_btn_pause: str
    svg_btn_play: str
    svg_btn_stop: str
    svg_app_icon: str
    collection_folder: str
    default_album_folder: str
    default_channel_volume: int
    auto_play: bool


def read_config(config_file: str) -> Config:
    with open(config_file) as file:
        data = json.load(file)
        return Config(**data)

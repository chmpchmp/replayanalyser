import configparser
from dotenv import load_dotenv
import os

SETTINGS_PATH = 'settings.ini'

class Settings:
    def __init__(self):
        settings = configparser.ConfigParser()
        settings.read(SETTINGS_PATH)
        load_dotenv()

        self.api_key = settings['DEFAULT']['api_key'] or os.getenv('api_key')
        self.osu_directory = settings['DEFAULT']['osu_directory'] or os.getenv('osu_directory')

        self.songs_directory = f'{self.osu_directory}\\Songs'
        self.replay_directory = f'{self.osu_directory}\\Replays'
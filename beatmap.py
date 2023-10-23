from replay import Replay

from dotenv import load_dotenv
import requests
import os
import pathlib

class Beatmap:
    def __init__(self, replay_path: str, songs_directory: str):
        self.replay_data = self.parse_replay_data(replay_path)
        self.beatmap_data = self.fetch_beatmap_data(self.replay_data['beatmap_hash'])
        self.beatmap_path = self.find_beatmap_path(songs_directory, self.beatmap_data['beatmapset_id'])
        print(self.beatmap_path)

    def parse_replay_data(self, replay_path: str) -> dict:
        replay_data = Replay(replay_path).decode_replay()

        if replay_data['game_mode'] != 0:
            raise ValueError('Game mode of the replay file is not osu!standard')
        
        return Replay(replay_path).decode_replay()

    def fetch_beatmap_data(self, beatmap_hash: str) -> int:
        load_dotenv()
        response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={os.getenv('api_key')}&h={beatmap_hash}")
        return response.json()[0]
    
    def find_beatmap_path(self, songs_directory: str, beatmap_id: str) -> None:
        subdirectories = os.listdir(songs_directory)

        for directory in subdirectories:
            if directory.split(' ')[0] == beatmap_id:
                return directory
        
        raise KeyError('Beatmap of replay cannot be found in songs directory')
    
if __name__ == '__main__':
    replay_path = r'sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr'
    songs_directory = r'C:\Users\snoop\AppData\Local\osu!\Songs'

    beatmap = Beatmap(replay_path, songs_directory)
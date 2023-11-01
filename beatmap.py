from replay import Replay

from dotenv import load_dotenv
import requests
import os
import pathlib

class Beatmap:
    def __init__(self, replay_path: str, songs_directory: str):
        self.replay = self.parse_replay_data(replay_path)
        self.cursor_data = self.replay.replay_data
        self.data = self.fetch_beatmap_data(self.replay.beatmap_hash)
        self.directory = self.find_beatmap_directory(songs_directory, self.data['beatmapset_id'])
        self.difficulty_data = self.fetch_difficulty_data(self.directory, self.data['beatmap_id'])
        self.hit_object_data = self.fetch_hit_object_data(self.difficulty_data)

        self.circle_radius = self.calculate_circle_radius(float(self.data['diff_size']))
        self.hit_window = self.calculate_hit_window(float(self.data['diff_overall']), int(self.replay.mods_used))

        self.title = self.create_beatmap_title()
    
    def parse_replay_data(self, replay_path: str) -> dict:
        replay = Replay(replay_path)

        if replay.game_mode == 0:
            return replay
        
        raise ValueError('Game mode of the replay file is not osu!standard')

    def fetch_beatmap_data(self, beatmap_hash: str) -> int:
        load_dotenv()
        response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={os.getenv('api_key')}&h={beatmap_hash}")
        return response.json()[0]
    
    def find_beatmap_directory(self, songs_directory: str, beatmapset_id: str) -> str:
        subdirectories = os.listdir(songs_directory)

        for directory in subdirectories:
            if directory.split(' ')[0] == beatmapset_id:
                return f'{songs_directory}\{directory}'
        
        raise KeyError('Beatmap of replay cannot be found in songs directory')
    
    def fetch_difficulty_data(self, beatmap_directory: str, beatmap_id: str) -> str:
        for file_name in os.listdir(beatmap_directory):
            if file_name.endswith('.osu'):
                file = open(pathlib.Path(f'{beatmap_directory}\{file_name}'), encoding = 'utf-8')
                data = file.read()
                for line in data.split('\n'):
                    if line == f'BeatmapID:{beatmap_id}':
                        file.close()
                        return data
                    
                file.close()

        raise KeyError('Beatmap file pertaining to the replay file cannot be found')
    
    def fetch_hit_object_data(self, difficulty_data: str) -> str:
        return [object.split(',')[:4] for object in difficulty_data.split('[HitObjects]')[1].split('\n')][1:-1]
    
    def calculate_circle_radius(self, circle_size: float) -> float:
        return 54.4 - 4.48 * circle_size
    
    def calculate_hit_window(self, overall_difficulty: float, mods_used: int) -> float:
        if mods_used & 64 == 64:    # hit window for double time mod (including nightcore)
            return (200 - 10 * overall_difficulty) / 1.5

        if mods_used & 256 == 256:    # hit window for half time mod
            return (200 - 10 * overall_difficulty) * 1.5

        return 200 - 10 * overall_difficulty
    
    def create_beatmap_title(self) -> str:
        return f"{self.data['artist']} - {self.data['title']} [{self.data['version']}]"
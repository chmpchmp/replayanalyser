from replay import Replay

from dotenv import load_dotenv
import requests
import os
import pathlib

class GameModeError(Exception):
    pass

class DirectoryError(Exception):
    pass

class Beatmap:
    def __init__(self, replay_path: str, songs_directory: str):
        self.replay = self.parse_replay_data(replay_path)
        self.cursor_data = self.calculate_cursor_timings(self.replay.replay_data)
        self.data = self.fetch_beatmap_data(self.replay.beatmap_hash)
        self.directory = self.find_beatmap_directory(songs_directory, self.data['beatmapset_id'])
        self.difficulty_data = self.fetch_difficulty_data(self.directory, self.data['beatmap_id'])
        self.hit_object_data = self.fetch_hit_object_data(self.difficulty_data, int(self.replay.mods_used))

        self.stack_leniency = self.fetch_stack_leniency(self.difficulty_data)
        self.circle_radius = self.calculate_circle_radius(float(self.data['diff_size']), int(self.replay.mods_used))
        self.hit_window = self.calculate_hit_window(float(self.data['diff_overall']), int(self.replay.mods_used))

        self.break_windows = self.fetch_break_windows(self.difficulty_data, self.cursor_data, self.hit_object_data, self.hit_window)

        self.title = self.create_beatmap_title()
    
    def parse_replay_data(self, replay_path: str) -> dict:
        replay = Replay(replay_path)

        if replay.game_mode == 0:
            return replay
        
        raise GameModeError('Game mode of the replay file is not osu!standard')
    
    def calculate_cursor_timings(self, cursor_data: list(list())) -> list(list()):
        cursor_timings = []
        
        ms_interval = 0

        for point in cursor_data:
            split_point = point.split('|')
            ms_interval += int(split_point[0])
            cursor_timings.append([ms_interval, float(split_point[1]), float(split_point[2]), int(split_point[3])])

        return cursor_timings
        return cursor_timings[1:-1]

    def fetch_beatmap_data(self, beatmap_hash: str) -> int:
        load_dotenv()
        response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={os.getenv('api_key')}&h={beatmap_hash}")
        return response.json()[0]
    
    def find_beatmap_directory(self, songs_directory: str, beatmapset_id: str) -> str:
        subdirectories = os.listdir(songs_directory)

        for directory in subdirectories:
            if directory.split(' ')[0] == beatmapset_id:
                return f'{songs_directory}\{directory}'
        
        raise DirectoryError('Beatmap of replay could not be found in songs directory')
    
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

        raise DirectoryError('Beatmap file pertaining to the replay file could not be found')
    
    def fetch_stack_leniency(self, difficulty_data: str) -> float:
        for line in difficulty_data.split('\n'):
            if 'StackLeniency: ' in line:
                return float(line[15:])

    def fetch_hit_object_data(self, difficulty_data: str, mods_used: int) -> list():
        hit_object_data = [object.split(',')[:4] for object in difficulty_data.split('[HitObjects]')[1].split('\n')][1:-1]
        hit_object_data = [[int(object[0]), int(object[1]), int(object[2]), int(object[3])] for object in hit_object_data
                            if int(object[3]) & 8 == 0]    # exclude objects that are spinners

        if mods_used & 16 == 16:    # invert hit objects across x-axis for hard rock
            for i in range(len(hit_object_data)):
                hit_object_data[i][1] = 384 - hit_object_data[i][1]

        return hit_object_data

    def calculate_circle_radius(self, circle_size: float, mods_used) -> float:
        if mods_used & 16 == 16:    # circle size for hard rock
            hr_circle_size = 1.3 * circle_size

            if hr_circle_size < 10:
                return (54.4 - 4.48 * hr_circle_size) 
            else:
                return (54.4 - 4.48 * 10)
        
        if mods_used & 256 == 256:    # circle size for easy
            return (54.4 - 4.48 * circle_size * 0.5)

        return 54.4 - 4.48 * circle_size
    
    def calculate_hit_window(self, overall_difficulty: float, mods_used: int) -> float:
        if mods_used & 16 == 16:    # hit window for hard rock
            hr_overall_difficulty = 1.4 * overall_difficulty

            if hr_overall_difficulty < 10:
                overall_difficulty = hr_overall_difficulty
            else:
                overall_difficulty = 10

        if mods_used & 256 == 256:    # hit window for easy
            overall_difficulty = 0.5 * overall_difficulty

        if mods_used & 64 == 64:    # hit window for double time (including nightcore)
            return (200 - 10 * overall_difficulty) / 1.5

        if mods_used & 256 == 256:    # hit window for half time
            return (200 - 10 * overall_difficulty) * 1.5

        return 200 - 10 * overall_difficulty
    
    def fetch_break_windows(self, difficulty_data: str, cursor_data: list(list()), hit_object_data: list(list()), hit_window) -> list(list()):
        break_windows = [window.split(',')[1:] for window in difficulty_data.split('//Break Periods')[1].split('//Storyboard Layer 0 (Background)')[0].split('\n')[1:-1]]

        for i in range(len(break_windows)):
            break_windows[i][0] = float(break_windows[i][0])
            break_windows[i][1] = float(break_windows[i][1])

        break_windows = [[cursor_data[1][0], hit_object_data[0][2] - hit_window]] + break_windows    # add from the beginning of beatmap to first note

        return break_windows
    
    def create_beatmap_title(self) -> str:
        return f"{self.data['artist']} - {self.data['title']} [{self.data['version']}]"
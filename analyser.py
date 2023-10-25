from beatmap import Beatmap

from dotenv import load_dotenv
import os

class Analyser:
    def __init__(self, replay_path: str, songs_directory: str):
        self.beatmap = Beatmap(replay_path, songs_directory)

        self.cursor_data = self.create_cursor_dictionary()
        self.hit_object_data = self.create_hit_object_dictionary()

        self.find_player_misses()

    def create_cursor_dictionary(self) -> dict():
        cursor_dictionary = dict()
        ms_interval = 0
        for point in self.beatmap.replay_data['byte_array']:
            split_list = point.split('|')
            ms_interval += int(split_list[0])
            cursor_dictionary[ms_interval] = split_list

        return cursor_dictionary
    
    def create_hit_object_dictionary(self) -> dict():
        return {int(hit_object[2]): hit_object for hit_object in self.beatmap.hit_object_data}

    def find_player_misses(self):
        ms_interval = 0
        
        while True:
            if ms_interval in self.cursor_data.keys() and ms_interval in self.hit_object_data.keys():
                print(ms_interval, self.cursor_data[ms_interval], self.hit_object_data[ms_interval])
                
            if ms_interval == 1000000:
                break
            ms_interval += 1

    def point_in_circle(self, center_x: int, center_y: int, radius: float, point_x: float, point_y: float) -> bool:
        return (point_x - center_x)**2 + (point_y - center_y)**2 < radius**2

if __name__ == '__main__':
    replay_path = r'sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr'
    replay_path = r'sample_replays\chmpchmp - Dove Cameron - LazyBaby [Hard] (2023-08-06) Osu.osr'
    
    load_dotenv()
    songs_directory = os.getenv('osu_songs_directory')

    Analyser(replay_path, songs_directory)
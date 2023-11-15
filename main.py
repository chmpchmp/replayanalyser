from analyser import Analyser
from display import Display

from dotenv import load_dotenv
import os

def run():
    replay_path = r"sample_replays\chmpchmp - kessoku band - Guitar to Kodoku to Aoi Hoshi [Akitoshi's Extreme] (2023-10-16) Osu.osr"
    replay_path = r"sample_replays\chmpchmp - ClariS - Hitorigoto -TV MIX- [Soliloquy] (2023-10-31) Osu.osr"
    
    load_dotenv()
    songs_directory = os.getenv('osu_songs_directory')

    analyser = Analyser(replay_path, songs_directory)
    display = Display(analyser.miss_data[0])
 
if __name__ == '__main__':
    run()


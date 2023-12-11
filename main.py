from settings import Settings
from analyser import Analyser
from display import Display

def main():
    settings = Settings()
    replay_path = r"sample_replays\chmpchmp - Sawai Miku - Colorful. (Asterisk DnB Remix) [Megumi] (2022-11-11) Osu.osr"

    analyser = Analyser(replay_path, settings.songs_directory)

    for i, miss in enumerate(analyser.miss_data):
        display = Display(miss, f'canvas/{i:06}')
 
if __name__ == '__main__':
    main()
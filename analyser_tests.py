from replay import Replay
from analyser import Analyser

from dotenv import load_dotenv
import os
import unittest

class AnalyserTestMethods(unittest.TestCase):
    # note: break_count - miss_count = sliderbreak_count
    def test_replay_01(self):
        replay_path = r"sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay_data = Replay(replay_path).decode_replay()
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay_data['miss_count'], beatmap.break_count)

    def test_replay_02(self):
        replay_path = r"sample_replays\chmpchmp - Hana - Sakura no Uta [Euphoria] (2023-01-27) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay_data = Replay(replay_path).decode_replay()
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay_data['miss_count'], beatmap.break_count)

    def test_replay_03(self):
        replay_path = r"sample_replays\chmpchmp - ClariS - Hitorigoto -TV MIX- [Soliloquy] (2023-10-31) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay_data = Replay(replay_path).decode_replay()
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay_data['miss_count'], beatmap.break_count - 1)
        
if __name__ == '__main__':
    unittest.main()

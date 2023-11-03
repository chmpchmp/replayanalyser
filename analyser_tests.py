from replay import Replay
from analyser import Analyser

from dotenv import load_dotenv
import os
import unittest

class AnalyserTestMethods(unittest.TestCase):

    def test_replay_01(self):
        replay_path = r"sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay.miss_count, beatmap.break_count)

    def test_replay_02(self):
        replay_path = r"sample_replays\chmpchmp - Hana - Sakura no Uta [Euphoria] (2023-01-27) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay.miss_count, beatmap.break_count)

    def test_replay_03(self):
        replay_path = r"sample_replays\chmpchmp - ClariS - Hitorigoto -TV MIX- [Soliloquy] (2023-10-31) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay.miss_count, beatmap.break_count - 1)

    def test_replay_04(self):
        replay_path = r"sample_replays\chmpchmp - RADWIMPS - Zen Zen Zense (movie ver.) [Extra Taki] (2023-11-02) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        #replay = Replay(replay_path)
        #beatmap = Analyser(replay_path, songs_directory)

        #self.assertEqual(replay.miss_count, beatmap.break_count - 1)

    def test_replay_05(self):
        replay_path = r"sample_replays\chmpchmp - RADWIMPS - Zen Zen Zense (movie ver.) [Extra Mitsuha] (2023-09-08) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay.miss_count, beatmap.break_count)

    def test_replay_06(self):
        replay_path = r"sample_replays\chmpchmp - 40mP feat. yuikonnu - Ame to Asphalt [Rain] (2023-11-03) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        beatmap = Analyser(replay_path, songs_directory)

        self.assertEqual(replay.miss_count, beatmap.break_count)
        
if __name__ == '__main__':
    unittest.main()

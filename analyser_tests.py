from replay import Replay
from analyser import Analyser

from dotenv import load_dotenv
import os
import unittest

class AnalyserTestMethods(unittest.TestCase):
    def test_replay_blade_dance(self):
        replay_path = r"sample_replays\chmpchmp - Ni-Sokkususu - Blade Dance [Kneesocks] (2023-10-21) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 26)
        self.assertEqual(analyser.key_two_count, 390)

        self.assertEqual(replay.miss_count, analyser.miss_count, 1)
        self.assertEqual(analyser.sliderbreak_count, 0)
        self.assertEqual(analyser.break_count, 1)

    def test_replay_sakura_no_uta(self):
        replay_path = r"sample_replays\chmpchmp - Hana - Sakura no Uta [Euphoria] (2023-01-27) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 97)
        self.assertEqual(analyser.key_two_count, 736)

        self.assertEqual(replay.miss_count, analyser.miss_count, 0)
        self.assertEqual(analyser.sliderbreak_count, 0)
        self.assertEqual(analyser.break_count, 0)

    def test_replay_hitorigoto(self):
        replay_path = r"sample_replays\chmpchmp - ClariS - Hitorigoto -TV MIX- [Soliloquy] (2023-10-31) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 19)
        self.assertEqual(analyser.key_two_count, 320)

        self.assertEqual(replay.miss_count, analyser.miss_count, 0)
        self.assertEqual(analyser.sliderbreak_count, 1)
        self.assertEqual(analyser.break_count, 1)

    def test_replay_ame_to_asphalt(self):
        replay_path = r"sample_replays\chmpchmp - 40mP feat. yuikonnu - Ame to Asphalt [Rain] (2023-11-03) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 10)
        self.assertEqual(analyser.key_two_count, 384)

        self.assertEqual(replay.miss_count, analyser.miss_count, 0)
        self.assertEqual(analyser.sliderbreak_count, 0)
        self.assertEqual(analyser.break_count, 0)

    def test_replay_flamingo(self):
        replay_path = r"sample_replays\chmpchmp - Kero Kero Bonito - Flamingo (WTN3 Remix) [Multi Color] (2023-11-05) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 79)
        self.assertEqual(analyser.key_two_count, 728)

        self.assertEqual(replay.miss_count, analyser.miss_count, 1)
        self.assertEqual(analyser.sliderbreak_count, 2)
        self.assertEqual(analyser.break_count, 3)

    def test_replay_super_nuko_world(self):
        replay_path = r"sample_replays\chmpchmp - yuikonnu & ayaponzu - Super Nuko World [Guy's Extra] (2023-11-05) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 331)
        self.assertEqual(analyser.key_two_count, 1033)

        self.assertEqual(replay.miss_count, analyser.miss_count, 0)
        self.assertEqual(analyser.sliderbreak_count, 4)
        self.assertEqual(analyser.break_count, 4)

    def test_replay_the_pretender(self):
        replay_path = r"sample_replays\chmpchmp - Infected Mushroom - The Pretender [Pretender] (2023-11-06) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 222)
        self.assertEqual(analyser.key_two_count, 1229)

        # replay.miss_count does not equal analyser.miss_count because the later does not count sliders missed
        self.assertEqual(analyser.miss_count, 2)
        self.assertEqual(analyser.sliderbreak_count, 9)
        self.assertEqual(analyser.break_count, 11)

    def test_replay_all_eyes_on_me(self):
        replay_path = r"sample_replays\chmpchmp - Fox Stevenson - All Eyes On Me (Cut Ver.) [Gracefully Hallucinate] (2023-11-08) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 89)
        self.assertEqual(analyser.key_two_count, 375)

        self.assertEqual(replay.miss_count, analyser.miss_count, 3)
        self.assertEqual(analyser.sliderbreak_count, 1)
        self.assertEqual(analyser.break_count, 4)

    def test_replay_sidetracked_day(self):
        replay_path = r"sample_replays\chmpchmp - VINXIS - Sidetracked Day [Daydream] (2023-10-29) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 323)
        self.assertEqual(analyser.key_two_count, 912)

        self.assertEqual(replay.miss_count, analyser.miss_count, 7)
        self.assertEqual(analyser.sliderbreak_count, 1)
        self.assertEqual(analyser.break_count, 8)

    def test_replay_lazybaby(self):
        replay_path = r"sample_replays\chmpchmp - Dove Cameron - LazyBaby [Hard] (2023-08-06) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 161)
        self.assertEqual(analyser.key_two_count, 344)

        self.assertEqual(replay.miss_count, analyser.miss_count, 0)
        self.assertEqual(analyser.sliderbreak_count, 0)
        self.assertEqual(analyser.break_count, 0)

    def test_replay_colorful(self):
        replay_path = r"sample_replays\chmpchmp - HAG - Colorful [Fiery's Extreme] (2023-10-27) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 35)
        self.assertEqual(analyser.key_two_count, 497)

        self.assertEqual(replay.miss_count, analyser.miss_count, 2)
        self.assertEqual(analyser.sliderbreak_count, 0)
        self.assertEqual(analyser.break_count, 2)

    def test_replay_colorful_dnb(self):
        replay_path = r"sample_replays\chmpchmp - Sawai Miku - Colorful. (Asterisk DnB Remix) [Megumi] (2022-11-11) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 121)
        self.assertEqual(analyser.key_two_count, 1172)

        self.assertEqual(replay.miss_count, analyser.miss_count, 13)
        self.assertEqual(analyser.sliderbreak_count, 2)
        self.assertEqual(analyser.break_count, 15)

    def test_replay_senpai(self):
        replay_path = r"sample_replays\chmpchmp - HoneyWorks meets TrySail - Senpai. [Graduation] (2023-11-05) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 173)
        self.assertEqual(analyser.key_two_count, 1160)

        self.assertEqual(replay.miss_count, analyser.miss_count, 17)
        self.assertEqual(analyser.sliderbreak_count, 3)
        self.assertEqual(analyser.break_count, 20)

    def test_replay_bocchi(self):
        replay_path = r"sample_replays\chmpchmp - kessoku band - Guitar to Kodoku to Aoi Hoshi [Akitoshi's Extreme] (2023-10-16) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 161)
        self.assertEqual(analyser.key_two_count, 804)

        self.assertEqual(replay.miss_count, analyser.miss_count, 2)
        self.assertEqual(analyser.sliderbreak_count, 1)
        self.assertEqual(analyser.break_count, 3)

    def test_replay_ikenai_borderline(self):
        replay_path = r"sample_replays\chmpchmp - WALKURE - Ikenai Borderline (Speed Up Ver.) [Your voice may even reach the heavens one day] (2023-04-28) Osu.osr"

        load_dotenv()
        songs_directory = os.getenv('osu_songs_directory')

        replay = Replay(replay_path)
        analyser = Analyser(replay_path, songs_directory)

        self.assertEqual(analyser.key_one_count, 145)
        self.assertEqual(analyser.key_two_count, 1145)

        # replay.miss_count does not equal analyser.miss_count because the later does not count sliders missed
        self.assertEqual(analyser.miss_count, 111)
        self.assertEqual(analyser.sliderbreak_count, 14)
        self.assertEqual(analyser.break_count, 125)

if __name__ == '__main__':
    unittest.main()

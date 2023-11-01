from replay import Replay
import unittest

class ReplayTestMethods(unittest.TestCase):

    def test_replay_01(self):
        path = 'sample_replays/chmpchmp - Suzuyu - Euphorium [The Dream Of White Star.] (2022-10-28) Osu.osr'
    
        replay_data = Replay(path).return_json()

        self.assertEqual(replay_data['game_mode'], 0)
        self.assertEqual(replay_data['player_name'], 'chmpchmp')
        self.assertEqual(replay_data['300_count'], 1136)
        self.assertEqual(replay_data['100_count'], 34)
        self.assertEqual(replay_data['50_count'], 0)
        self.assertEqual(replay_data['geki_count'], 239)
        self.assertEqual(replay_data['katu_count'], 25)
        self.assertEqual(replay_data['miss_count'], 4)
        self.assertEqual(replay_data['total_score'], 15729060)
        self.assertEqual(replay_data['highest_combo'], 746)
        self.assertEqual(replay_data['perfect_combo'], 0)
        self.assertEqual(replay_data['mods_used'], 0)
        self.assertEqual(replay_data['online_score_id'], 4303493392)

    def test_replay_02(self):
        path = "sample_replays/chmpchmp - gmtn. (witch's slave) - furioso melodia [Wrath] (2023-05-05) Osu.osr"
    
        replay_data = Replay(path).return_json()

        self.assertEqual(replay_data['game_mode'], 0)
        self.assertEqual(replay_data['player_name'], 'chmpchmp')
        self.assertEqual(replay_data['300_count'], 1174)
        self.assertEqual(replay_data['100_count'], 270)
        self.assertEqual(replay_data['50_count'], 59)
        self.assertEqual(replay_data['geki_count'], 217)
        self.assertEqual(replay_data['katu_count'], 113)
        self.assertEqual(replay_data['miss_count'], 168)
        self.assertEqual(replay_data['total_score'], 2179090)
        self.assertEqual(replay_data['highest_combo'], 252)
        self.assertEqual(replay_data['perfect_combo'], 0)
        self.assertEqual(replay_data['mods_used'], 1)
        self.assertEqual(replay_data['online_score_id'], 4431925699)

    def test_replay_03(self):
        path = "sample_replays/chmpchmp - Dove Cameron - LazyBaby [Hard] (2023-08-06) Osu.osr"
    
        replay_data = Replay(path).return_json()

        self.assertEqual(replay_data['game_mode'], 0)
        self.assertEqual(replay_data['player_name'], 'chmpchmp')
        self.assertEqual(replay_data['300_count'], 489)
        self.assertEqual(replay_data['100_count'], 14)
        self.assertEqual(replay_data['50_count'], 1)
        self.assertEqual(replay_data['geki_count'], 86)
        self.assertEqual(replay_data['katu_count'], 11)
        self.assertEqual(replay_data['miss_count'], 0)
        self.assertEqual(replay_data['total_score'], 10961313)
        self.assertEqual(replay_data['highest_combo'], 776)
        self.assertEqual(replay_data['perfect_combo'], 0)
        self.assertEqual(replay_data['mods_used'], 72)
        self.assertEqual(replay_data['online_score_id'], 4485390023)

if __name__ == '__main__':
    unittest.main()

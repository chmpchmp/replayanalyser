import pathlib
import struct
import lzma

class Replay:
    def __init__(self, path: str):
        self.data = self.open_file(path)
        self.offset = 0

        self.game_mode = self.decode_data('b')
        self.game_version = self.decode_data('i')
        self.beatmap_hash = self.decode_string()
        self.player_name = self.decode_string()
        self.replay_hash = self.decode_string()
        self.count_300 = self.decode_data('h')
        self.count_100 = self.decode_data('h')
        self.count_50 = self.decode_data('h')
        self.geki_count = self.decode_data('h')
        self.katu_count = self.decode_data('h')
        self.miss_count = self.decode_data('h')
        self.total_score = self.decode_data('i')
        self.highest_combo = self.decode_data('h')
        self.perfect_combo = self.decode_data('b')
        self.mods_used = self.decode_data('i')
        self.life_bar_graph = self.decode_string().strip(',').split(',')
        self.time_stamp = self.decode_data('q')
        self.byte_length = self.decode_data('i')
        self.replay_data = self.decode_lzma(self.byte_length).split(',')[1:-1]
        self.online_score_id = self.decode_data('q')
        self.target_practice_mod = None
        
        if self.mods_used & 8388608 == 8388608:
            self.target_practice_mod = self.decode_data('d')

    def open_file(self, path: str) -> bytes:
        file = open(pathlib.Path(path), 'rb')
        data = file.read()
        file.close()
        return data
    
    def decode_data(self, data_type: str) -> int:
        output = struct.unpack_from(data_type, self.data, self.offset)
        self.offset += struct.calcsize(data_type)
        return output[0]    # output will always be in a tuple of size 1
    
    def decode_string(self) -> str:
        if self.data[self.offset] == 0x00:
            self.offset += 1
        elif self.data[self.offset] == 0x0b:
            self.offset += 1
            length = self.decode_uleb128()
            self.offset += 1
            string = self.data[self.offset:self.offset+length].decode('utf-8')
            self.offset += length
            return string
        else:
            raise ValueError('Initial value is ', self.data[self.offset], ', expected 0x00 or 0x0b')
        
    def decode_uleb128(self) -> int:
        '''
        Converts a value in unsigned little endian base 128 to decimal
        '''
        output = 0
        iteration = 0
        
        while True:
            value = self.data[self.offset]
            chunk = value & 0b01111111          # ignore the most significant bit
            output += chunk << iteration * 7    # insert the chunk into the output value
            if value < 0b10000000:              # exit loop if the most significant bit is zero
                break
            iteration += 1                      # constant to multiple by 7
            self.offset += 1                    # shift to next byte

        return output
    
    def decode_lzma(self, byte_length: int) -> str:
        return str(lzma.decompress(self.decode_data(f'<{byte_length}s')))
    
    def return_json(self) -> dict():
        replay_data = dict()
        replay_data['game_mode'] = self.game_mode
        replay_data['game_version'] = self.game_version
        replay_data['beatmap_hash'] = self.beatmap_hash
        replay_data['player_name'] = self.player_name
        replay_data['replay_hash'] = self.replay_hash
        replay_data['300_count'] = self.count_300
        replay_data['100_count'] = self.count_100
        replay_data['50_count'] = self.count_50
        replay_data['geki_count'] = self.geki_count
        replay_data['katu_count'] = self.katu_count
        replay_data['miss_count'] = self.miss_count
        replay_data['total_score'] = self.total_score
        replay_data['highest_combo'] = self.highest_combo
        replay_data['perfect_combo'] = self.perfect_combo
        replay_data['mods_used'] = self.mods_used
        replay_data['life_bar_graph'] = self.life_bar_graph
        replay_data['time_stamp'] = self.time_stamp
        replay_data['byte_length'] = self.byte_length
        replay_data['replay_data'] = self.replay_data
        replay_data['online_score_id'] = self.online_score_id
        
        if self.target_practice_mod != None:
            replay_data['target_practice_mod'] = self.target_practice_mod
        return replay_data 
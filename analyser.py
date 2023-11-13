from beatmap import Beatmap

class Analyser:
    # to do: account for breaks from leaving sliderball and leaving buzzslider too early

    def __init__(self, replay_path: str, songs_directory: str):
        self.beatmap = Beatmap(replay_path, songs_directory)

        self.key_one_count = 0
        self.key_two_count = 0

        # the amount of combo breaks because of sliders
        self.miss_count = 0

        # the amount of combo breaks because of sliders
        self.sliderbreak_count = 0

        # miss_count plus sliderbreak_count
        self.break_count = 0

        self.analyze_replay()

        print(self.miss_count, self.sliderbreak_count, self.break_count)

    def analyze_replay(self) -> None:
        active_cursor_points = self.fetch_active_cursor_points(self.beatmap.cursor_data)
        hit_object_data = self.beatmap.hit_object_data

        previous_hit = [0, -1, -1, -1]

        for object in hit_object_data:
            possible_points = self.calculate_points_within_timing(object[2], self.beatmap.hit_window, previous_hit[0], active_cursor_points)
            possible_points = self.calculate_points_in_circle(object[0], object[1], self.beatmap.circle_radius, possible_points)

            if previous_hit in possible_points:
                possible_points.remove(previous_hit)

            if possible_points == [] and object[3] & 1 == 1:
                self.miss_count += 1
                self.break_count += 1

                # set the window to the maximum timing to account for notelock
                previous_hit = [object[2] + self.beatmap.hit_window, -1, -1, -1]
            elif possible_points == [] and object[3] & 2 == 2:
                self.sliderbreak_count += 1
                self.break_count += 1

                # set the window to the maximum timing to account for notelock
                previous_hit = [object[2] + self.beatmap.hit_window, -1, -1, -1]
            else:
                previous_hit = possible_points[0]

    def fetch_active_cursor_points(self, cursor_timings: list(list())) -> list(list()):
        active_cursor_points = []

        for i in range(len(cursor_timings)-1):
            if self.detect_key_one(cursor_timings[i][3], cursor_timings[i+1][3]) and not self.in_interval(cursor_timings[i+1][0], self.beatmap.break_windows):
                active_cursor_points.append(cursor_timings[i+1])
                self.key_one_count += 1

            if self.detect_key_two(cursor_timings[i][3], cursor_timings[i+1][3]) and not self.in_interval(cursor_timings[i+1][0], self.beatmap.break_windows):
                active_cursor_points.append(cursor_timings[i+1])
                self.key_two_count += 1

        return active_cursor_points
    
    def in_interval(self, value: int, intervals: list(list())) -> bool:
        for interval in intervals:
            if interval[0] <= value <= interval[1]:
                return True
            
        return False

    def detect_key_one(self, first_timing: int, second_timing: int) -> bool:
        return first_timing & 1 == 0 and second_timing & 1 == 1
    
    def detect_key_two(self, first_timing: int, second_timing: int) -> bool:
        return first_timing & 2 == 0 and second_timing & 2 == 2
    
    def calculate_points_within_timing(self, object_timing: float, hit_window: float, previous_hit_timing: float, cursor_points: list) -> list:
        minimum_timing = previous_hit_timing
        maximum_timing = object_timing + hit_window
        return [point for point in cursor_points if minimum_timing < point[0] < maximum_timing]
    
    def calculate_points_in_circle(self, center_x: int, center_y: int, radius: float, cursor_points: list) -> list:
        return [point for point in cursor_points if (point[1] - center_x)**2 + (point[2] - center_y)**2 < radius**2]
    
if __name__ == '__main__':
    from replay import Replay

    from dotenv import load_dotenv
    import os

    replay_path = r"C:\Users\snoop\AppData\Local\osu!\Replays\chmpchmp - CHiCO with HoneyWorks - Kessen Spirit [Not DT Farmer's Extra] (2023-01-16) Osu.osr"

    load_dotenv()
    songs_directory = os.getenv('osu_songs_directory')

    replay = Replay(replay_path)
    analyser = Analyser(replay_path, songs_directory)

from beatmap import Beatmap

class Analyser:
    def __init__(self, replay_path: str, songs_directory: str):
        self.beatmap = Beatmap(replay_path, songs_directory)

        self.key_one_count = 0
        self.key_two_count = 0

        self.miss_count = 0
        self.sliderbreak_count = 0
        self.break_count = 0

        self.analyze_replay()

    def analyze_replay(self):
        cursor_timings = self.beatmap.cursor_data
        active_cursor_points = self.fetch_active_cursor_points(cursor_timings)
        hit_object_data = self.beatmap.hit_object_data

        print(self.key_one_count, self.key_two_count, len(active_cursor_points))

    def fetch_active_cursor_points(self, cursor_timings: list(list())) -> list(list()):
        active_cursor_points = []

        for i in range(len(cursor_timings)-1):
            if self.detect_key_one(cursor_timings[i][3], cursor_timings[i+1][3]) and cursor_timings[i+1][0] >= 0 and cursor_timings[i+1][3] != 1058002 and not self.in_interval(cursor_timings[i+1][0], self.beatmap.break_windows):
                active_cursor_points.append(cursor_timings[i+1])
                self.key_one_count += 1

            if self.detect_key_two(cursor_timings[i][3], cursor_timings[i+1][3]) and cursor_timings[i+1][0] >= 0 and cursor_timings[i+1][3] != 1058002 and not self.in_interval(cursor_timings[i+1][0], self.beatmap.break_windows):
                active_cursor_points.append(cursor_timings[i+1])
                self.key_two_count += 1

        return active_cursor_points
    
    def in_interval(self, value: int, intervals: list(list())) -> bool:
        for interval in intervals:
            if interval[0] <= value <= interval[1]:
                return True
            
        return False

    def detect_key_one(self, first_timing: int, second_timing: int) -> bool:
        return (first_timing ^ 1) & (second_timing & 1) == 1
    
    def detect_key_two(self, first_timing: int, second_timing: int) -> bool:
        return (first_timing ^ 2) & (second_timing & 2) == 2
    
    def calculate_valid_cursor_points(self, object_timing: float, hit_window: float, active_cursor_points: dict) -> dict:
        minimum_timing = object_timing - hit_window
        maximum_timing = object_timing + hit_window
        return [point for point in active_cursor_points if minimum_timing < point[0] < maximum_timing]
    
    def detect_miss(self, center_x: int, center_y: int, circle_radius: float, valid_cursor_points: list(list())) -> bool:
        for point in valid_cursor_points:
            if self.point_in_circle(center_x, center_y, circle_radius, point[1], point[2]):
                return False
        
        return True

    def point_in_circle(self, center_x: int, center_y: int, radius: float, point_x: float, point_y: float) -> bool:
        return (point_x - center_x)**2 + (point_y - center_y)**2 < radius**2
from beatmap import Beatmap
from miss import Miss

MILLISECOND_INTERVAL = 300

class Analyser:
    def __init__(self, replay_path: str, songs_directory: str):
        self.beatmap = Beatmap(replay_path, songs_directory)

        self.key_one_count = 0
        self.key_two_count = 0

        self.miss_count = 0          # the amount of combo breaks because of hit circles
        self.slidermiss_count = 0    # the amount of combo breaks because of sliders
        self.break_count = 0         # miss_count plus slidermiss

        self.miss_data = []

        self.analyze_replay()

        #print(self.miss_count, self.sliderbreak_count, self.break_count)

    def analyze_replay(self) -> None:
        # to do: account for hit window changes after breaks
        # to do: account for breaks from leaving sliderball and leaving buzzslider too early

        active_cursor_points = self.fetch_active_cursor_points(self.beatmap.cursor_data)
        hit_object_data = self.beatmap.hit_object_data
        cursor_data = self.beatmap.cursor_data
        circle_radius = self.beatmap.circle_radius

        # set the window to the minimum timing of the first hit object
        previous_hit = [hit_object_data[0][2] - self.beatmap.hit_window, -1, -1, -1]

        for i in range(len(hit_object_data)):
            if hit_object_data[i][3] & 8 == 8 and i == len(hit_object_data) - 1:
                pass
            # set the window to the minimum timing of the next hit object and avoid miss checking if the current object is a spinner
            elif hit_object_data[i][3] & 8 == 8:
                previous_hit = [hit_object_data[i+1][2] - self.beatmap.hit_window, -1, -1, -1]
            else:
                # notelock misses occur when the input comes between the current object's minimum timing and previous object's maximum timing
                possible_points = self.calculate_points_within_timing(hit_object_data[i][2], self.beatmap.hit_window, previous_hit[0], active_cursor_points)
                possible_points = self.calculate_points_in_circle(hit_object_data[i][0], hit_object_data[i][1], self.beatmap.circle_radius, possible_points)

                if previous_hit in possible_points:
                    possible_points.remove(previous_hit)

                if possible_points == []:
                    self.increment_miss_count(hit_object_data[i][3])

                    miss_hit_object_data = [object for object in hit_object_data if hit_object_data[i][2] - MILLISECOND_INTERVAL <= object[2] <= hit_object_data[i][2] + MILLISECOND_INTERVAL]
                    miss_cursor_data = [point for point in cursor_data if hit_object_data[i][2] - MILLISECOND_INTERVAL <= point[0] <= hit_object_data[i][2] + MILLISECOND_INTERVAL]
                    miss_cursor_input_data = [point for point in active_cursor_points if hit_object_data[i][2] - MILLISECOND_INTERVAL <= point[0] <= hit_object_data[i][2] + MILLISECOND_INTERVAL]

                    self.miss_data.append(Miss(miss_hit_object_data, miss_cursor_data, hit_object_data[i][2], miss_cursor_input_data, circle_radius))

                    # set the window to the maximum timing to account for notelock
                    previous_hit = [hit_object_data[i][2] + self.beatmap.hit_window, -1, -1, -1]
                else:
                    previous_hit = possible_points[0]

    def fetch_active_cursor_points(self, cursor_timings: list(list())) -> list(list()):
        active_cursor_points = []

        for i in range(len(cursor_timings)-1):
            if not self.in_interval(cursor_timings[i+1][0], self.beatmap.break_windows):
                # do not track inputs during breaks
                if self.detect_key_one(cursor_timings[i][3], cursor_timings[i+1][3]):
                    active_cursor_points.append(cursor_timings[i+1])
                    self.key_one_count += 1

                if self.detect_key_two(cursor_timings[i][3], cursor_timings[i+1][3]):
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
    
    def calculate_points_within_timing(self, object_timing: float, hit_window: float, previous_max_hit_timing: float, cursor_points: list) -> list:
        minimum_timing = previous_max_hit_timing
        maximum_timing = object_timing + hit_window
        return [point for point in cursor_points if minimum_timing < point[0] < maximum_timing]
    
    def calculate_points_in_circle(self, center_x: int, center_y: int, radius: float, cursor_points: list) -> list:
        return [point for point in cursor_points if (point[1] - center_x)**2 + (point[2] - center_y)**2 < radius**2]

    def increment_miss_count(self, object_type: int) -> None:
        if object_type & 1 == 1:
            self.miss_count += 1
        if object_type & 2 == 2:
            self.slidermiss_count += 1

        self.break_count += 1
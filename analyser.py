from beatmap import Beatmap

from dotenv import load_dotenv
import os

class Analyser:
    def __init__(self, replay_path: str, songs_directory: str):
        self.beatmap = Beatmap(replay_path, songs_directory)
        self.miss_count = 0
        self.sliderbreak_count = 0
        self.break_count = 0

        self.analyze_replay()

    def analyze_replay(self):
        cursor_timings = self.beatmap.cursor_data
        active_cursor_points = self.fetch_active_cursor_points(cursor_timings)
        hit_object_data = self.beatmap.hit_object_data

        for object in hit_object_data:
            valid_cursor_points = self.calculate_valid_cursor_points(object[2], self.beatmap.hit_window, active_cursor_points)

            if self.detect_miss(object[0], object[1], self.beatmap.circle_radius, valid_cursor_points):
                if object[2] & 1 == 1:
                    self.miss_count += 1

                if object[2] & 2 == 2:
                    self.sliderbreak_count += 1
                    
                self.break_count += 1
                #print("Combo break detected!")

    def fetch_active_cursor_points(self, cursor_timings: list(list())) -> list(list()):
        active_cursor_points = []

        for i in range(len(cursor_timings)-1):
            if self.detect_key_press(cursor_timings[i][3], cursor_timings[i+1][3]) and cursor_timings[i+1][0] >= 0 and cursor_timings[i+1][3] != 1058002:
                active_cursor_points.append(cursor_timings[i+1])

        return active_cursor_points

    def detect_key_press(self, first_input: int, second_input: int) -> bool:
        key_one = (first_input ^ 1) & (second_input & 1) == 1
        key_two = (first_input ^ 2) & (second_input & 2) == 2
        return key_one or key_two
    
    def calculate_valid_cursor_points(self, object_timing: float, hit_window: float, active_cursor_points: dict) -> dict:
        minimum_timing = object_timing - hit_window
        maximum_timing = object_timing + hit_window
        return [point for point in active_cursor_points if point[0] > minimum_timing and point[0] < maximum_timing]
    
    def detect_miss(self, center_x: int, center_y: int, circle_radius: float, valid_cursor_points: list(list())) -> bool:
        for point in valid_cursor_points:
            if self.point_in_circle(center_x, center_y, circle_radius, point[1], point[2]):
                return False
        
        return True

    def point_in_circle(self, center_x: int, center_y: int, radius: float, point_x: float, point_y: float) -> bool:
        return (point_x - center_x)**2 + (point_y - center_y)**2 < radius**2
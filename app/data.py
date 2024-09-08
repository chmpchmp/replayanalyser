from settings import Settings
from analyser import Analyser
from canvas import Canvas
from exception import APIKeyError, GameModeError, DirectoryError

import os

FRAMES_DIRECTORY = 'frames'

class Data:
    def __init__(self, replay_path: str, width: int, height: int):
        settings = Settings()

        self.beatmap_title = ''
        self.break_count = 0
        self.miss_timings = []

        self.check_directory(FRAMES_DIRECTORY)
        self.clear_directory(FRAMES_DIRECTORY)

        try:
            analyser = Analyser(replay_path, settings.songs_directory)

            self.generate_frames(FRAMES_DIRECTORY, analyser.miss_data, width, height)

            self.beatmap_title = analyser.beatmap.title
            self.break_count = analyser.break_count

            for miss in analyser.miss_data:
                self.miss_timings.append(miss.hit_object_timing)
                
            self.status_message = 'Replay analysis complete!'
        except APIKeyError as message:
            self.status_message = f'ERROR: {str(message)}'
        except GameModeError as message:
            self.status_message = f'ERROR: {str(message)}'
        except DirectoryError as message:
            self.status_message = f'ERROR: {str(message)}'

    @staticmethod
    def check_directory(directory: str) -> None:
        if not os.path.exists(directory):
            os.mkdir(directory)

    @staticmethod
    def clear_directory(directory: str) -> None:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def generate_frames(directory: str, miss_data: list, width: int, height: int) -> None:
        for i, miss in enumerate(miss_data):
            canvas = Canvas(miss, width, height)
            canvas.export(directory, i)
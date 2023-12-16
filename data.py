from settings import Settings
from analyser import Analyser
from canvas import Canvas
from exception import APIKeyError, GameModeError, DirectoryError

import os

FRAMES_DIRECTORY = 'frames'

class Data:
    def __init__(self, replay_path: str):
        settings = Settings()

        self.beatmap_title = ''
        self.miss_count = 0

        try:
            analyser = Analyser(replay_path, settings.songs_directory)

            self.check_directory(FRAMES_DIRECTORY)
            self.clear_directory(FRAMES_DIRECTORY)
            self.generate_frames(FRAMES_DIRECTORY, analyser.miss_data)

            self.beatmap_title = analyser.beatmap.title
            self.miss_count = analyser.miss_count

            self.status = 'Replay analysis complete!'
        except APIKeyError as message:
            self.status = f'ERROR: {str(message)}'
        except GameModeError as message:
            self.status = f'ERROR: {str(message)}'
        except DirectoryError as message:
            self.status = f'ERROR: {str(message)}'

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
    def generate_frames(directory: str, miss_data: list) -> None:
        for i, miss in enumerate(miss_data):
            canvas = Canvas(miss)
            canvas.export(directory, i)
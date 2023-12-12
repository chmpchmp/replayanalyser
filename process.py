from settings import Settings
from analyser import Analyser
from canvas import Canvas

import os

class Process:
    def __init__(self, replay_path: str):
        settings = Settings()
        analyser = Analyser(replay_path, settings.songs_directory)

        directory = 'canvas'

        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            
            if os.path.isfile(file_path):
                os.remove(file_path)

        for i, miss in enumerate(analyser.miss_data):
            canvas = Canvas(miss)
            canvas.export(f'canvas\{i:06}')
from settings import Settings
from analyser import Analyser
from canvas import Canvas

class Process:
    def __init__(self, replay_path: str):
        settings = Settings()
        analyser = Analyser(replay_path, settings.songs_directory)

        for i, miss in enumerate(analyser.miss_data):
            canvas = Canvas(miss)
            canvas.export(f'canvas\{i:06}')
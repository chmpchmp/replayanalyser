from settings import Settings
from analyser import Analyser
from display import Display

def run():

    settings = Settings()
    replay_path = input()

    analyser = Analyser(replay_path, Settings().songs_directory)
    display = Display(analyser.miss_data[0])
 
if __name__ == '__main__':
    run()


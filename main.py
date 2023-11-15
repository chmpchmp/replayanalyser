from settings import Settings
from analyser import Analyser
from display import Display

def run():

    settings = Settings()
    replay_path = input()
    index = int(input())

    analyser = Analyser(replay_path, Settings().songs_directory)
    display = Display(analyser.miss_data[index])
 
if __name__ == '__main__':
    run()


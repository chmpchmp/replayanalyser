import PyQt5.QtWidgets as qtw

from settings import Settings
from data import Data

class Window(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_width = 1280
        self.window_height = 720
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle('replayanalyser')

        self.button = qtw.QPushButton(self)
        self.button.clicked.connect(self.select_file_clicker)

        self.show()

    def select_file_clicker(self) -> None:
        settings = Settings()
        file_name = qtw.QFileDialog.getOpenFileName(caption = 'Select a replay', directory = settings.replay_directory, filter = '*.osr')
        replay_path = file_name[0]
        
        if replay_path != '':
            self.run_analyser(replay_path)
            print('Analysing replay...')

    @staticmethod
    def run_analyser(replay_path: str) -> None:
        data = Data(replay_path)
 
if __name__ == '__main__':
    app = qtw.QApplication([])
    window = Window()
    app.exec_()
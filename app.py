from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

from settings import Settings
from data import Data

class Window(QWidget):
    def __init__(self):
        super().__init__()

        window_width = 1280
        window_height = 720
        self.setFixedSize(window_width, window_height)
        self.setWindowIcon(QIcon('assets\\favicon.png'))
        self.setWindowTitle('replayanalyser')

        layout = QVBoxLayout()

        self.beatmap_title = QLabel('Title')

        self.file_number = 0
        self.max_file_number = 0

        self.image = QLabel()
        self.image.setAlignment(QtCore.Qt.AlignCenter)

        self.previous_frame_button = QPushButton('Previous frame')
        self.previous_frame_button.clicked.connect(self.select_previous_frame)
        self.previous_frame_button.setEnabled(False)

        self.next_frame_button = QPushButton('Next frame')
        self.next_frame_button.clicked.connect(self.select_next_frame)
        self.next_frame_button.setEnabled(False)

        self.select_file_button = QPushButton('Select replay')
        self.select_file_button.clicked.connect(self.select_file_clicker)

        self.status = QLabel('Status')
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.beatmap_title)
        layout.addWidget(self.image)
        layout.addWidget(self.previous_frame_button)
        layout.addWidget(self.next_frame_button)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def select_file_clicker(self) -> None:
        self.status.setText('Analysing replay...')
        settings = Settings()
        file_name = QFileDialog.getOpenFileName(caption = 'Select a replay', directory = settings.replay_directory, filter = '*.osr')
        replay_path = file_name[0]
        
        if replay_path != '':
            data = Data(replay_path)
            self.beatmap_title.setText(data.beatmap_title)
            self.file_number = 0
            self.max_file_number = data.miss_count - 1
            self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

            if self.max_file_number != 0:
                self.next_frame_button.setEnabled(True)
                
            self.status.setText(data.status)

    def select_previous_frame(self) -> None:
        if self.file_number >= self.max_file_number:
            self.next_frame_button.setEnabled(True)

        self.file_number -= 1
        self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

        if self.file_number <= 0:
            self.previous_frame_button.setEnabled(False)

    def select_next_frame(self) -> None:
        if self.file_number <= 0:
            self.previous_frame_button.setEnabled(True)

        self.file_number += 1
        self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

        if self.file_number >= self.max_file_number:
            self.next_frame_button.setEnabled(False)
        
if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
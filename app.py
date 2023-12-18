from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5 import QtCore

from settings import Settings
from data import Data

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.window_width = 1280
        self.window_height = 720
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowIcon(QIcon('assets\\favicon.png'))
        self.setWindowTitle('replayanalyser')

        self.file_number = -1
        self.max_file_number = -1
        self.miss_timings = []

        layout = QVBoxLayout()
        core_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        self.beatmap_title = QLabel()
        self.beatmap_title.setFont(QFont('Arial Bold', 12))

        self.image = QLabel()
        self.image.setPixmap(QPixmap())
        self.image.setAlignment(QtCore.Qt.AlignCenter)

        self.select_replay_button = QPushButton('Select replay')
        self.select_replay_button.clicked.connect(self.select_replay_clicker)

        self.previous_frame_button = QPushButton('Previous frame')
        self.previous_frame_button.clicked.connect(self.select_previous_frame)
        self.previous_frame_button.setEnabled(False)

        self.next_frame_button = QPushButton('Next frame')
        self.next_frame_button.clicked.connect(self.select_next_frame)
        self.next_frame_button.setEnabled(False)

        self.break_label = QLabel()
        self.break_label.setAlignment(QtCore.Qt.AlignCenter)
        self.update_break_count()

        self.timing_label = QLabel()
        self.timing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.update_timing_count()

        self.status = QLabel()
        self.status.setText('No replay selected')
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        buttons_layout.addWidget(self.select_replay_button, 1)
        buttons_layout.addWidget(QLabel(), 5)
        buttons_layout.addWidget(self.previous_frame_button, 1)
        buttons_layout.addWidget(self.next_frame_button, 1)
        buttons_layout.addWidget(self.break_label, 1)
        buttons_layout.addWidget(self.timing_label, 1)
        buttons_layout.addWidget(QLabel(), 40)

        core_layout.addLayout(buttons_layout, 10)
        core_layout.addWidget(self.image, 90)

        layout.addWidget(self.beatmap_title, 5)
        layout.addLayout(core_layout, 90)
        layout.addWidget(self.status, 5)

        self.setLayout(layout)
        
    def select_replay_clicker(self) -> None:
        settings = Settings()
        file_name = QFileDialog.getOpenFileName(caption = 'Select a replay', directory = settings.replay_directory, filter = '*.osr')
        replay_path = file_name[0]
        
        if replay_path != '':
            self.status.setText('Analysing replay...')
            data = Data(replay_path, int(0.85 * self.window_width), int(0.85 * self.window_height))
            self.max_file_number = data.break_count - 1
            self.beatmap_title.setText(data.beatmap_title)

            self.previous_frame_button.setEnabled(False)

            # when a full combo or error is detected
            if self.max_file_number == -1:
                self.next_frame_button.setEnabled(False)
                self.file_number = -1
                self.image.setPixmap(QPixmap())
            
            # when there is only one break
            elif self.max_file_number == 0:
                self.next_frame_button.setEnabled(False)
                self.file_number = 0
                self.miss_timings = data.miss_timings
                self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

            # when there is more than one break
            else:
                self.next_frame_button.setEnabled(True)
                self.file_number = 0
                self.miss_timings = data.miss_timings
                self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

            self.update_break_count()
            self.update_timing_count()
                
            self.status.setText(data.status_message)

    def select_previous_frame(self) -> None:
        if self.file_number >= self.max_file_number:
            self.next_frame_button.setEnabled(True)

        self.file_number -= 1
        self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

        if self.file_number <= 0:
            self.previous_frame_button.setEnabled(False)

        self.update_break_count()
        self.update_timing_count()

    def select_next_frame(self) -> None:
        if self.file_number <= 0:
            self.previous_frame_button.setEnabled(True)

        self.file_number += 1
        self.image.setPixmap(QPixmap(f'frames\\{self.file_number:06}.png'))

        if self.file_number >= self.max_file_number:
            self.next_frame_button.setEnabled(False)

        self.update_break_count()
        self.update_timing_count()

    def update_break_count(self) -> None:
        if self.file_number == -1:
            self.break_label.setText('')
        else:
            self.break_label.setText(f'Miss: {str(self.file_number+1)}/{str(self.max_file_number+1)}')

    def update_timing_count(self) -> None:
        if self.file_number == -1:
            self.timing_label.setText('')
        else:
            self.timing_label.setText(f'Time: {self.convert_milliseconds(self.miss_timings[self.file_number])}')

    @staticmethod
    def convert_milliseconds(ms: int) -> str:
        milliseconds = ms % 1000
        seconds = int((ms / 1000) % 60)
        minutes = int(ms / (1000 * 60))
        return f'{minutes:02}:{seconds:02}.{milliseconds:03}'

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
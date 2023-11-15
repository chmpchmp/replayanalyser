import configparser

class Settings:
    def __init__(self):
        settings = configparser.ConfigParser()
        settings.read('settings.ini')

        self.api_key = settings['DEFAULT']['api_key']
        self.osu_directory = settings['DEFAULT']['osu_directory']
        self.songs_directory = f'{self.osu_directory}\Songs'
        self.replay_directory = f'{self.osu_directory}\Replays'

        print(self.api_key)
        print(self.osu_directory)
        print(self.songs_directory)
        print(self.replay_directory)

if __name__ == '__main__':
    Settings()
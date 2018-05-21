from DataManagement.FileManager import FileManager
from DataManagement.PathBuilders import *

class SoundRepository:
    def __init__(self):
        self.file_manager = FileManager()
        self.path_builder_init = SoundPathBuilder

    def add_sound(self, user_name, training_number, sound):
        path_builder = self.path_builder_init(user_name, training_number)
        self.file_manager.create_wav(sound, path_builder)

    def get_sound(self, user_name, training_number):
        path_builder = self.path_builder_init(user_name, training_number)
        sound = self.file_manager.get_wav(path_builder)
        return sound
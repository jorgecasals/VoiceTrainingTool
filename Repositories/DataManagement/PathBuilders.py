import DataPaths

class DataPathBuilder:
    def __init__(self):
        self.path = DataPaths.DATA_DIR

class TrainingsDirPathBuilder:
    def __init__(self, user_name):
        self.path = DataPaths.TRAININGS_DIR.format(user_name)

class TrainingFilePathBuilder:
    def __init__(self, user_name, training_number):
        self.path = DataPaths.TRAINING_INFO_FILE.format(user_name, training_number)

class UsersPathBuilder:
    def __init__(self):
        self.path = DataPaths.USERS_DIR

class UserFilesPathBuilder:
    def __init__(self, user_name):
        self.path = DataPaths.USER_FILE.format(user_name)

class LtasPathBuilder:
    def __init__(self, user_name, training_number):
        self.path = DataPaths.LTAS_FILE.format(user_name, training_number)

class SpectrumPathBuilder:
    def __init__(self, user_name, training_number):
        self.path = DataPaths.SPECTRUM_FILE.format(user_name, training_number)

class SoundPathBuilder:
    def __init__(self, user_name, training_number):
        self.path = DataPaths.SOUND_FILE.format(user_name, training_number)

class ReadingsDirPathBuilder:
    def __init__(self):
        self.path = DataPaths.READINGS_DIR

class ReadingFileInfoPathBuilder:
    def __init__(self, reading_title):
        self.path = DataPaths.READING_FILE.format(reading_title)


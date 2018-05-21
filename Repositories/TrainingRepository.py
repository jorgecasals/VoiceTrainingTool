from Entities.Training import Training
from datetime import datetime
from DataManagement.FileManager import FileManager
from DataManagement.PathBuilders import *
from DataManagement.JsonConverter import JsonConverter
from DataManagement.DataConstants import *

class TrainingRepository:
    def __init__(self):
        self.fileManager = FileManager()

    def get_trainings_by_user_name(self, user_name):
        dir_path_builder = TrainingsDirPathBuilder(user_name)
        training_names = self.fileManager.get_all_names(dir_path_builder)
        trainings = []

        for training_name in training_names:
            training_path_builder = TrainingFilePathBuilder(user_name, training_name)
            training_json = self.fileManager.get_content(training_path_builder)
            json_converter = JsonConverter(Training)
            training = json_converter.convert_from_json(training_json)
            trainings.append(training)

        return trainings

    def add_training(self, training):
        dir_path_builder = TrainingsDirPathBuilder(training.user_name)
        self.fileManager.create_dir(str(training.number), dir_path_builder)
        info_path_builder = TrainingFilePathBuilder(training.user_name, training.number)
        json_converter = JsonConverter(Training)
        json_training = json_converter.convert_to_json(training)
        self.fileManager.create(json_training, info_path_builder)

    def add_training_folder(self, user_name):
        dir_path_builder = UserFilesPathBuilder(user_name)
        self.fileManager.create_dir(TRAININGS, dir_path_builder)

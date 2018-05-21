from DataManagement.FileManager import FileManager
from DataManagement.JsonConverter import JsonConverter

class TrainingDataRepository:
    def __init__(self, path_builder_init, data_init):
        self.file_manager = FileManager()
        self.path_builder_init = path_builder_init
        self.data_init = data_init

    def add_data(self, user_name, training_number, data):
        path_builder = self.path_builder_init(user_name, training_number)
        json_converter = JsonConverter(self.data_init)
        json_data = json_converter.convert_to_json(data)
        self.file_manager.create(json_data, path_builder)

    def get_data(self, user_name, training_number):
        path_builder = self.path_builder_init(user_name, training_number)
        json_data = self.file_manager.get_content(path_builder)
        json_converter = JsonConverter(self.data_init)
        data = json_converter.convert_from_json(json_data)
        return data
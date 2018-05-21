from DataManagement.FileManager import FileManager
from DataManagement.PathBuilders import UsersPathBuilder
from DataManagement.PathBuilders import UserFilesPathBuilder

class UserRepository:
    def __init__(self):
        self.file_manager = FileManager()
        self.path_builder = UsersPathBuilder()

    def get_users(self):
        users_names = self.file_manager.get_all_names(self.path_builder)
        return users_names

    def add_user(self, user_name):
        self.file_manager.create_dir(user_name, self.path_builder)

    def exist(self, user_name):
        path_to_user_dir = UserFilesPathBuilder(user_name)
        user_exist = self.file_manager.exist(path_to_user_dir)
        return user_exist
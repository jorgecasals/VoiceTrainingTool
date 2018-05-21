class UserService:
    def __init__(self, user_repository, training_repository):
        self.user_repository = user_repository
        self.training_repository = training_repository

    def get_all_users_names(self):
        users_names = self.user_repository.get_users()
        return users_names

    def create_user(self, user_name):
        if not self.user_repository.exist(user_name):
            self.user_repository.add_user(user_name)
            self.training_repository.add_training_folder(user_name)

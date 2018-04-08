class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_all_users_names(self):
        users_names = self.user_repository.get_users()
        return users_names

    def create_user(self, user_name):
        users_names = self.user_repository.get_users()
        if user_name not in users_names:
            self.user_repository.add_user(user_name)
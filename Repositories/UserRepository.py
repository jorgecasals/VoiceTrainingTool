class UserRepository:
    def __init__(self):
        self.users = ['Jorge', 'Cary', 'Elisabeth']

    def get_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)
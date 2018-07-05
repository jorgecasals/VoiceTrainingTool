class RepositoryCache:
    def __init__(self):
        self.data_dict = {}

    def add_data(self, keys, data):
        self.data_dict[keys, data]

    def clear(self):
        self.data_dict = {}

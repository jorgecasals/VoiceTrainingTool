class RepositoryCache:
    def __init__(self):
        self.data_dict = {}

    def add_data(self, keys, data):
        self.data_dict[keys, data]

    def clear(self):
        self.data_dict = {}

    def is_data_cached(self, keys):
        result = self.data_dict.has_key(keys)
        return result

    def get_data(self, keys):
        result = self.data_dict[keys]
        return result

Cache = RepositoryCache()

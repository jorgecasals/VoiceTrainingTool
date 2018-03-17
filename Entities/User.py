class User:
    def __init__(self, name, password, email):
        self.email = email
        self.password = password
        self.name = name
        self.records = []

    def add_record(self, record):
        self.records.append(record)


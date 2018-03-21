import datetime

class Record:
    def __init__(self, sound, text_read, projection_level):
        self.sound = sound;
        self.creation_date = datetime.datetime.now()
        self.text_read = text_read
        self.projection_level = projection_level

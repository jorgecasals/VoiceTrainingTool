import datetime

class Record:
    def __init__(self, sound, text_read):
        self.sound = sound;
        self.creation_date = datetime.datetime.now()
        self.text_read = text_read
        self.projection_level = 0

    def set_projection_level(self, projection_level):
        self.projection_level = projection_level
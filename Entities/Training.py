import datetime

class Training:
    def __init__(self, number= None, reading_title= None, user_name= None, creation_date = None, time_dedicated = None):
        self.number = number
        self.reading_title = reading_title
        self.user_name = user_name
        self.time_dedicated = time_dedicated
        if creation_date != None:
            self.creation_date = creation_date
        else :
            self.creation_date = datetime.datetime.now()
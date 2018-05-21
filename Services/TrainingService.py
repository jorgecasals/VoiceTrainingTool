class TrainingService:
    def __init__(self, training_repository, user_repository, reading_repository, sound_repository):
        self.training_repository = training_repository
        self.user_repository = user_repository
        self.reading_repository = reading_repository
        self.sound_repository = sound_repository

    def get_previous_training_of_user(self, user_name):
        trainings = self.training_repository.get_trainings_by_user_name(user_name)
        return trainings

    def create_training(self, training, sound):
        user_exist = self.user_repository.exist(training.user_name)
        if user_exist:
            self.training_repository.add_training(training)
            self.sound_repository.add_sound(training.user_name, training.number, sound)

    def get_readings_for_training(self):
        lectures = self.reading_repository.get_available_readings()
        return lectures

    def get_reading(self, reading_title):
        reading = self.reading_repository.get_reading(reading_title)
        return reading

    def get_sound_of_training(self, username, training_number):
        sound = self.sound_repository.get_sound(username, training_number)
        return sound
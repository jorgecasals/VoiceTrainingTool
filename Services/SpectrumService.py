from Algorithms import SoundAlgorithms
from Entities.Audio import Audio
import numpy
from Algorithms.SpectrumCreator import SpectrumCreator

class SpectrumService:
    def __init__(self, spectrum_repository, sound_repository):
        self.spectrum_repository = spectrum_repository
        self.sound_repository = sound_repository

    def create_spectrum(self, user_name, training_number):
        sound = self.sound_repository.get_sound(user_name, training_number)
        spectrum = SoundAlgorithms().calculate_spectrum_from_sound(sound)
        self.spectrum_repository.add_data(user_name, training_number, spectrum)

    def get_spectrum(self, user_name, training_number):
        spectrum = self.spectrum_repository.get_data(user_name, training_number)
        return spectrum
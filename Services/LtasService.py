from Algorithms.SoundAlgorithms import SoundAlgorithms
from Entities.Audio import Audio
import numpy
from Algorithms.SpectrumCreator import SpectrumCreator
from Algorithms.LtasCreator import LtasCreator

import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")

class LtasService:
    def __init__(self, ltas_repository, sound_repository):
        self.ltas_repository = ltas_repository
        self.sound_repository = sound_repository

    def get_ltas(self, user_name, training_number):
        ltas = self.ltas_repository.get_data(user_name, training_number)
        return ltas

    def create_ltas(self, user_name, training_number):
        sound = self.sound_repository.get_sound(user_name, training_number)
        ltas = SoundAlgorithms().calculate_ltas_from_sound(sound)
        self.ltas_repository.add_data(user_name, training_number, ltas)
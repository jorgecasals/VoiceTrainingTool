import Entities.Spectrum
import Entities.Sound
import Entities.SoundValue
import Common.Constants

class SoundToSpectrumTransformer:
    def __init__(self):
        pass

    def transform_sound_to_spectrum(self, sound, fast):
        samples_number = sound.get_samples_total()
        if fast:
            total_samples = self.get_minor_2pow_greater_than(samples_number)
        frequencies_number = samples_number/2 + 1
        frecuency_step = 1.0 / (sound.sampling_period * samples_number)
        max_frequency = 0.5 / sound.sampling_period
        min_frequency = - max_frequency



    def get_minor_2pow_greater_than(self, total):
        return total
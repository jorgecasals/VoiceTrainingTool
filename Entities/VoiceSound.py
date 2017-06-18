from Entities.VoiceSpectrum import VoiceSpectrum
from FurierTransformer import FurierTransformer
from Logger import Logger

class VoiceSound:


    def __init__(self, values, user, date):
        self.values = values
        self.user = user
        self.date = date


    @Logger.log_it
    def BuildSpectrum(self):
        furier_transformer = FurierTransformer(c.FRAMES_PER_BUFFER, c.RATE)
        frequencies_power = furier_transformer.get_frequency_power(self.values)
        return VoiceSpectrum(complex_values=frequencies_power, user=self.user, date=self.date)


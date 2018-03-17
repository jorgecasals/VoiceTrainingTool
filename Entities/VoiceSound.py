from Entities.VoiceSpectrum import VoiceSpectrum
from FurierTransformer import FurierTransformer
from Logger import Logger


class VoiceSound:


    def __init__(self, values, user, date):
        self.values = values
        self.user = user
        self.date = date


    @Logger.log_it
    def build_spectrum(self):pass
        # transformer = FurierTransformer(len(self.values), Constants.RATE)
        # frequencies_power = transformer.transform(self.values)
        # spectrum = VoiceSpectrum(complex_values=frequencies_power, user=self.user, date=self.date)
        # return spectrum


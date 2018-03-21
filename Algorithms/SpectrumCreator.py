import numpy
from Common.Constants import *
from Entities.Spectrum import Spectrum

class SpectrumCreator:
    def __init__(self):
        pass

    def create_spectrum_from_audio(self, audio):
        min_pow_greater_than_data = self.get_min_pow_greater_than_number(len(audio.values))
        audio_values = list(audio.values)
        data = numpy.append(audio_values, ([0] * (min_pow_greater_than_data - len(audio_values))))
        scale = (float(RATE) / float(len(data)))
        fft_data = numpy.fft.fft(data)
        fft_data = fft_data * scale * SCALE_TO_BE_SAME_AS_PRAAT
        xs = numpy.arange(len(data) / 2, dtype=float)
        i = int((len(data) / 2))
        fft_data = fft_data[:i]
        # TODO: it should be in the constructor of the object spectrum
        frequency_step = float(RATE) / len(data)
        xs = xs[:i] * frequency_step
        spectrum = Spectrum(frequencies=xs, values=fft_data, frequency_step=frequency_step)
        return spectrum

    def get_min_pow_greater_than_number(self, number):
        pow = 1
        while pow < number:
            pow *= 2

        return pow
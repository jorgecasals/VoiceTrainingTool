import numpy

from Algorithms.LtasCreator import LtasCreator
from Algorithms.SpectrumCreator import SpectrumCreator
from Entities.Audio import Audio


class SoundAlgorithms:

    def __init__(self):
        pass

    def calculate_ltas_from_sound(self, sound):
        spectrum = self.calculate_spectrum_from_sound(sound)
        ltas = self.calculate_ltas_from_spectrum(spectrum)
        return ltas

    def calculate_spectrum_from_sound(self, sound):
        sound_buffer = self.convert_sound_list_to_buffer(sound)
        byte_frames_audio = numpy.fromstring(sound_buffer, dtype=numpy.int16)
        audio = Audio(byte_frames_audio)
        spectrum = SpectrumCreator().create_spectrum_from_audio(audio)
        return spectrum

    def calculate_ltas_from_spectrum(self, spectrum):
        ltas = LtasCreator().create_ltas_from_spectrum(spectrum)
        return ltas

    def convert_sound_list_to_buffer(self, sound):
        buffer_sound = ''
        for frame in sound:
            buffer_sound += frame

        return buffer_sound
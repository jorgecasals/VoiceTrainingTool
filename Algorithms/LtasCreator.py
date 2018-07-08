from Common.Constants import *
from math import ceil
import numpy
from Entities.Ltas import Ltas

class LtasCreator:
    def __init__(self):
        pass

    def create_ltas_from_spectrum(self, spectrum):
        bands_number = int(ceil(max_frequency / BANDWIDTH)) - 1
        ltas_values = [0] * bands_number
        for banda in range(0, bands_number):
            initial_band_frequency = banda * BANDWIDTH
            mean_energy_density = spectrum.get_mean_energy_density(initial_band_frequency, initial_band_frequency + BANDWIDTH)
            mean_power_density = mean_energy_density * spectrum.frequency_step
            ltas_values[banda] = -300.0 if mean_power_density == 0.0 else numpy.multiply(10, numpy.log10(mean_power_density / 4.0e-10))

        bands = numpy.arange(bands_number, dtype=float) * BANDWIDTH
        ltas = Ltas(bands=bands, values=ltas_values, bandwidth = BANDWIDTH)
        return ltas
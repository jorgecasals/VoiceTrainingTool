from sys import maxint
from Algorithms.FrequencyBin import FrequencyBin
from Entities.Ltas import Ltas

class ProjectionCalculator:
    def __init__(self):

        #TODO: Put the numeric values in a contants file.
        self.projection_bin = FrequencyBin(initial_kHz=3, end_kHz=4)
        self.projection_surrounding_bin = FrequencyBin(initial_kHz=2, end_kHz=5)

    #the minimum ltas bands number is 22.
    def measure_projection(self, ltas):

        projection_area = self.get_area_from_ltas(ltas, self.projection_bin)
        surrounding_area = self.get_area_from_ltas(ltas, self.projection_surrounding_bin)
        projection_value = (projection_area/surrounding_area) * 10

        return projection_value

    def get_area_from_ltas(self, ltas, area_bin):
        ltas_bands_number = len(ltas.bands)
        bands_per_1000_hz = ltas_bands_number / 22
        starting_frequency = bands_per_1000_hz * area_bin.initial_kHz
        final_frequency = bands_per_1000_hz * area_bin.end_kHz
        ltas_value_in_projection_bands = 0

        for projection_band_index in range(starting_frequency, final_frequency):
            ltas_value_in_projection_bands += ltas.values[projection_band_index]

        area = ltas_value_in_projection_bands

        return area




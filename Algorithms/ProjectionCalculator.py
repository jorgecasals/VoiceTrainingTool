from Entities.Ltas import Ltas

class ProjectionCalculator:
    def __init__(self):
        self.initial_frequency_value = 3
        self.final_frequency_value = 4
    #the minimum ltas bands number is 22.
    def measure_projection(self, ltas):
        ltas_bands_number = len(ltas.bands)
        bands_per_1000_hz = ltas_bands_number / 22
        starting_frequency = bands_per_1000_hz * self.initial_frequency_value
        final_frequency = bands_per_1000_hz * self.final_frequency_value
        ltas_value_in_projection_bands = 0
        for projection_band_index in range(starting_frequency, final_frequency):
            ltas_value_in_projection_bands += ltas.values[projection_band_index]

        #need to see if this is gonna work.
        projection_value = ltas_value_in_projection_bands * ltas.bandwidth

        return projection_value

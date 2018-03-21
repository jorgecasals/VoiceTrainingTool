import numpy

class Spectrum:
    def __init__(self, frequencies, values, frequency_step):
        self.frequencies = frequencies
        self.values = values
        self.frequency_step = frequency_step

    def get_mean_energy_density(self, min_frequency, max_frequency):
        (values_sum, values_range) = self.get_sum_range(min_frequency, max_frequency);
        return values_sum / values_range;

    def get_sum_range(self, min_frequency, max_frequency):

        samples_number_to_min = self.get_samples_number_beggining_to_frequency(min_frequency)
        samples_number_to_max = self.get_samples_number_beggining_to_frequency(max_frequency)
        samples_total = float(len(self.frequencies))
        if samples_number_to_max < 0.5 or samples_number_to_min >= samples_total + 0.5:
            return 0.0, 0.0

        values_sum = 0.0
        values_range = 0.0
        samples_number_to_min_rounded = int(
            0 if samples_number_to_min < 0.5 else round(samples_number_to_min))
        samples_number_to_max_rounded = int(
            samples_total if samples_number_to_max >= (samples_total + 0.5) else round(
                samples_number_to_max))

        for index in range(samples_number_to_min_rounded + 1, samples_number_to_max_rounded):
            value = self.get_energy_density(index)
            values_range += 1.0
            values_sum += value

        if samples_number_to_min_rounded == samples_number_to_max_rounded:
            value = self.get_energy_density(samples_number_to_min_rounded)
            value_range = samples_number_to_max - samples_number_to_min
            values_range += value_range
            values_sum += value_range * value
        else:
            if samples_number_to_min_rounded >= 1:
                value = self.get_energy_density(samples_number_to_min_rounded)
                value_range = samples_number_to_min_rounded - samples_number_to_min + 0.5
                values_range += value_range
                values_sum += value_range * value
            if samples_number_to_max_rounded < samples_total:
                value = self.get_energy_density(samples_number_to_max_rounded)
                value_range = samples_number_to_max - samples_number_to_max_rounded + 0.5
                values_range += value_range
                values_sum += value_range * value

        return values_sum, values_range

    def get_samples_number_beggining_to_frequency(self, frequency):
        result = frequency / self.frequency_step + 1.0
        return result

    def get_energy_density(self, frequency_index):
        complex = self.values[frequency_index]
        energy_density = 2.0 * (complex.real * complex.real + complex.imag * complex.imag)
        return energy_density

    def get_absolute_values(self):
        return numpy.abs(self.values)

'''
    Attributes:
	xmin              // Start time (seconds).
	xmax              // End time (seconds).
	nx                // Number of samples.
	dx                // Sampling period (seconds).
	x1                // Time of first sample (seconds).
	ymin == 1         // Left or only channel.
	ymax              // Right or only channels.
	ny                // Number of channels.
	dy == 1; y1 == 1  // y is channel number (1 = left or mono; 2 = right).
	z [i] [...]       // Amplitude.
	z may be replaced (e.g., in pasting).
'''
import math
from Spectrum import *
from Ltas import *

class SoundAnalyzer:
    def __init__(self):
        pass

    def perform_ltas_analysis(self, sound, bandwidth):
        spectrum = self.sound_to_spectrum(sound, True)#true is for Fast
        ltas = self.spectrum_to_ltas(spectrum.get(), bandwidth)
        self.apply_correction(sound, spectrum, ltas)

        return ltas

    def apply_correction(self, sound, spectrum, ltas):
        correction = -10.0 * self.log10(spectrum.samplin_period_seconds * sound.samples_number * sound.samplin_period_seconds)
        for iband in range(ltas.samples_number):#iband originally is 1 bigger
            ltas.intensity_per_band[1][iband] += correction #TODO: Create type ltas with amplitude property.

    def sound_to_spectrum(self, sound, fast):
        numberOfSamples = sound.samples_number
        if(fast):
            numberOfSamples = 2;
            while(numberOfSamples < sound.samples_number):
                numberOfSamples *= 2

        numberOfFrequencies = numberOfSamples / 2 + 1

        #TODO: We need to touch here in order to save the furier transformation in data

        data = [None]*numberOfSamples#initializing a list with numberOfSamples lenght
        fourierTable = self.initialize_furier_table(numberOfSamples)
        for index in range(1, numberOfSamples):
            data[index] = sound.amplitude[1][index] if sound.channel_number == 1 else 0.5 * (sound.amplitude[1][index] + sound.amplitude[2][index])

        self.fill_furier_data(fourierTable, data)

        spectrum = Spectrum(highest_frequency= 0.5 / sound.samplin_period_seconds, number_of_frequencies=numberOfFrequencies);
        spectrum.frequency_step = 1.0 / (sound.samplin_period_seconds * numberOfSamples);
        real_values = spectrum.amplitude[spectrum.reals_row];
        imaginary_values = spectrum.amplitude[spectrum.imaginary_row];
        scaling = sound.samplin_period_seconds;
        real_values[1] = data[1] * scaling;
        imaginary_values[1] = 0.0;

        for index in range(2, numberOfFrequencies):
            real_values[index] = data[index + index - 2] * scaling; # data[2], data[4], ...
            imaginary_values[index] = data[index + index - 1] * scaling; # data[3], data[5], ...

        if ((numberOfSamples & 1) != 0) :
            if (numberOfSamples > 1) :
                real_values[numberOfFrequencies] = data[numberOfSamples - 1] * scaling;
                imaginary_values[numberOfFrequencies] = data[numberOfSamples] * scaling;
        else:
            real_values[numberOfFrequencies] = data[numberOfSamples] * scaling;
            imaginary_values[numberOfFrequencies] = 0.0;

        return spectrum;

    def spectrum_to_ltas(self, spectrum, band_width):
        number_of_bands = math.ceil((spectrum.highest_frequency - spectrum.lowest_frequency) / band_width)
        if band_width <= spectrum.frequency_step:
            raise ValueError("Bandwidth: {0} must be greater than frequency_step {1}".format(band_width, spectrum.frequency_step))
        ltas = Ltas(number_of_bands, band_width)
        self.matrix_init(ltas, spectrum.xmin, spectrum.xmax, number_of_bands, band_width, spectrum.xmin + 0.5 * band_width, 1.0, 1.0, 1, 1.0, 1.0)

        for iband in range(1, number_of_bands):
            start_frequency = ltas.lowest_frequency + (iband - 1) * band_width;
            mean_energy_density = self.get_mean_energy_density (spectrum, start_frequency, start_frequency + band_width, 0, 1);
            mean_power_density = mean_energy_density * spectrum.frequency_step; # as an approximation for a division by the original duration
            ltas.intensity_per_band[1][iband] = -300.0 if mean_power_density == 0.0 else 10.0 * self.log10(mean_power_density / 4.0e-10);

        return ltas;

    def log10(self, number):
        return math.log10(number)

    #TODO: These is furier (TTF) algorithm to be used by the above methods.
    def initialize_furier_table(self, numberOfSamples):
        pass

    def fill_furier_data(self, fourierTable, data):
        pass

    #TODO: finish until the following checkin.
    #ilevel = 0 y unit = 1
    def get_mean_energy_density(self, spectrum, start_frequency, end_frequency):
        start_frequency_index = self.get_index(spectrum, start_frequency)
        end_frequency_index = self.get_index(spectrum, end_frequency)
        definition_range = 0
        total = 0
        if end_frequency_index >= 0.5 & start_frequency_index < spectrum.number_of_frequencies:
            imin = 0 if start_frequency_index < 0.5 else math.floor(start_frequency_index + 0.5)
            imax = spectrum.number_of_frequencies if end_frequency_index >= spectrum.number_of_frequencies + 0.5 else math.floor(end_frequency_index + 0.5)
            for sample_index in range(imin + 1, imax):
                value = spectrum.get_value(imin, level=0, unit=1)
                if self.isan(value):#TODO: Avoid this checks
                    definition_range += 1.0
                    total += value
            if imin == imax:
                value = spectrum.get_value(imin)
                if self.isan(value):
                    phase = end_frequency_index - start_frequency_index
                    definition_range += phase
                    total += phase * value
            else :
                if imin >= 1:
                    value = spectrum.get_value(imin)
                    if self.isan(value):
                        phase = imin - start_frequency_index + 0.5
                        definition_range += phase
                        total += phase * value
                if imax <= spectrum.number_of_frequencies:
                    value = spectrum.get_value(imax)
                    if self.isan(value):
                        phase = end_frequency_index - imax + 0.5
                        definition_range += phase
                        sum  = phase * value

        return total/definition_range if definition_range > 0 else None

    def matrix_init(self, ltas, xmin, xmax, number_of_bands, band_width, param, param1, param2, param3, param4, param5):
        pass

    def get_index(self, spectrum, frequency):
        return (frequency - spectrum.x1)/spectrum.frequency_step + 1.0

    def isan(self, number):
        return number == number



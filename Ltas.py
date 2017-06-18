#TODO: Create in every class the unit of the variable (Hz, db/Hz, etc)
#TODO: create a guard utility for checking parameters
import math


class Ltas:
    '''

	Attributes:
		xmin				// Minimum frequency (Hz).
		xmax > xmin		// Maximum frequency (Hz).
		nx >= 1			// Number of bands.
		dx > 0.0			// Band width (Hz).
		x1				// Centre of first band (Hz).
		ymin, ymax, dy, y1 = 1.0
		ny = 1
		z [1] [1..nx]		// The power spectral density per band, in db/Hz.

    '''

    def _init_(self, spectrum, number_of_bands, band_width):
        self._init_(number_of_bands, band_width)
        self.lowest_frequency = 0.0
        self.highest_frequency = number_of_bands * band_width
        # TODO: To see if the property below is the same as this in spectrum: self.number_of_frequencies = number_of_frequencies
        self.number_of_bands = number_of_bands
        self.band_width = band_width
        self.center_of_first_band = 0.5 * band_width  # TODO: Search in SoundAnalizer if we are doing this with a parameter to the spectrum constructor.
        self.initialize_intensity_per_band(spectrum)

    def initialize_intensity_per_band(self, spectrum):
        number_of_bands = math.ceil((spectrum.highest_frequency - spectrum.lowest_frequency) / self.band_width)
        if self.band_width <= spectrum.frequency_step:
            raise ValueError(
                "Bandwidth: {0} must be greater than frequency_step {1}".format(self.band_width, spectrum.frequency_step))
        ltas = Ltas(number_of_bands, self.band_width)
        self.matrix_init(ltas, spectrum.xmin, spectrum.xmax, number_of_bands, self.band_width,
                         spectrum.xmin + 0.5 * self.band_width, 1.0, 1.0, 1, 1.0, 1.0)

        for iband in range(1, number_of_bands):
            start_frequency = ltas.lowest_frequency + (iband - 1) * self.band_width;
            mean_energy_density = self.get_mean_energy_density(spectrum, start_frequency, start_frequency + self.band_width,
                                                               0, 1);
            mean_power_density = mean_energy_density * spectrum.frequency_step;  # as an approximation for a division by the original duration
            ltas.intensity_per_band[1][iband] = -300.0 if mean_power_density == 0.0 else 10.0 * self.log10(
                mean_power_density / 4.0e-10);

        return ltas;
#TODO: Create in every class the unit of the variable (Hz, db/Hz, etc)
#TODO: create a guard utility for checking parameters
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
		z [1] [1..nx]		// The intensity per band, in db/Hz.

    '''
    def _init_(self, number_of_bands, band_width):

        self.lowest_frequency = 0.0
        self.highest_frequency = number_of_bands * band_width
        #TODO: To see if the property below is the same as this in spectrum: self.number_of_frequencies = number_of_frequencies
        self.number_of_bands = number_of_bands
        self.band_width = band_width
        self.center_of_first_band = 0.5 * band_width #TODO: Search in SoundAnalizer if we are doing this with a parameter to the spectrum constructor.
        
        self.initialize_intensity_per_band()

    def initialize_intensity_per_band(self):
        #TODO: Original code stablish this value: 1e-4 instead of: 0 it said: "straight tube, area 1 cm2."
        self.intensity_per_band = [[0 for y in xrange(self.number_of_bands)]]
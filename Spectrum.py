import math

class Spectrum:
    '''
    	xmin            // lowest frequency (Hz)
    	xmax            // highest frequency (Hz)
    	nx              // number of frequencies
    	dx              // frequency step (Hz)
    	x1              // first frequency (Hz)
    	ymin = 1.0      // first row: real part
    	ymax = 2.0      // second row: imaginary part
    	ny = 2          // two rows
    	dy = y1 = 1.0   // y is row number
    '''

    def __init__(self, highest_frequency, number_of_frequencies):
        if highest_frequency <= 0 or number_of_frequencies < 2:
            raise ValueError(
                "Highest frequency should be greater than 0 "
                "and number of frequencies sould be greater than 2, "
                "actual values are Highest frequency : {0} and number of frequencies: {1}".format(highest_frequency,
                                                                                                  number_of_frequencies))

        self.lowest_frequency = 0.0
        self.highest_frequency = highest_frequency
        self.number_of_frequencies = number_of_frequencies
        self.frequency_step = highest_frequency / (number_of_frequencies - 1)
        self.first_frequency = 0.0
        self.reals_row = 1.0
        self.imaginary_row = 2.0
        self.number_of_rows = 2
        self.row_number = 1.0
        self.initialize_amplitude()

    def initialize_amplitude(self):
        #TODO: Possible solution : d = numpy.empty((n, 0)).tolist()
        self.amplitudes = [[0 for y in xrange(self.number_of_frequencies)] for x in xrange(self.number_of_rows)]

    def get_value(self, index, level, units):
        energy_density = 2.0* (math.pow(self.amplitudes[1][index], 2) + math.pow(self.amplitudes[2][index], 2))
        return energy_density
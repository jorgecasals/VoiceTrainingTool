''' Attributes:
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

class Sound:
    def __init__(self, number_of_channels, start_time, end_time, number_of_samples, samplin_period, time_of_first_sample):
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_samples = number_of_samples
        self.samplin_period = samplin_period
        self.time_of_first_sample = time_of_first_sample #TODO: Verify in execution: is always 1
        self.left_channel = 1 #TODO: need to see utility of this properties
        self.right_channel = number_of_channels
        self.number_of_channels = number_of_channels
        self.sampling_period_seconds = 1.0
        self.initialize_data()

    def __init__(self, audio_data, number_of_channels, start_time, end_time, number_of_samples, samplin_period, time_of_first_sample):
        self.audio_data = audio_data
        self.__init__(number_of_channels, start_time, end_time, number_of_samples, samplin_period, time_of_first_sample)

    def initialize_data(self):
        self.data = [[0 for y in xrange(self.number_of_samples)] for x in xrange(self.number_of_channels)]

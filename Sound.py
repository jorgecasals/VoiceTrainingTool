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
    def __init__(self, audio_data, number_of_channels, start_time, end_time, number_of_samples, sampling_period, time_of_first_sample):
        #TODO: maybe is convenient to separate time and values.
        self.audio_data = audio_data
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_samples = number_of_samples
        self.sampling_period = sampling_period
        self.time_of_first_sample = time_of_first_sample  # TODO: Verify in execution: is always 1
        self.left_channel = 1  # TODO: need to see utility of this properties
        self.right_channel = number_of_channels
        self.number_of_channels = number_of_channels
        self.sampling_period_seconds = 1.0



import Common.Constants as Constants
import sys

class SpectrumValue:
    def __init__(self, frequency, real, img):

        self.img = img
        self.real = real
        if frequency < Constants.min_frequency or frequency > Constants.max_frequency:
            raise ValueError("The Frequency value needs to be between {0} and {1}".format(Constants.min_frequency, Constants.max_frequency))
        self.frequency = frequency


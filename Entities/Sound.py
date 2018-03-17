import SoundValue

class Sound:
    def __init__(self, sampling_period):
        self.sampling_period = sampling_period
        self.values = []

    def add_amplitud(self, amplitude):
        value = SoundValue(time=self.values.count()*self.sampling_period, amplitude=amplitude)
        self.values.append(value)#TODO: Apply solution in spectrum to insert it in order if it's not greater

    def get_samples_total(self):
        return self.values.count()



import Entities.SpectrumValue

class Spectrum:
    def __init__(self):
        self.values = []

    def add_value(self, value):
        #values_lenght = self.values.count()
        #if values_lenght > 0 and self.values[values_lenght - 1].frequency > value.frequency:
        #    self.insert_value_in_ordered(value)
        #else:
        self.values.append(value)

    def insert_value_in_ordered(self, value):
        for values_index in xrange(start=0, stop=self.values.count()):
            spectrum_value = self.values[values_index]
            if spectrum_value.frequency > value.frequency:
                self.values.insert(values_index, value)
                break


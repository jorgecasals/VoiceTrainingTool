class Ltas:
    def __init__(self, bands = None, values = None, bandwidth = None):
        self.bands = bands
        self.values = values
        self.bandwidth = bandwidth

    def get_ltas_normalized(self, min_value):
        values_copy = self.values[:]

        if min_value < 0:
            values_copy = map(lambda value: value - min_value, self.values)
            values_copy = map(lambda value: value / (- min_value), values_copy)

        if min_value > 0:
            values_copy = map(lambda value: value / min_value, values_copy)

        return Ltas(self.bands, values_copy, self.bandwidth)

    def get_min_value(self):
        return min(self.values)
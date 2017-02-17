import numpy

class FurierTransformer:
    def __init__(self, buffer_size, rate):
        self.buffer_size = buffer_size
        self.rate = rate

    @staticmethod
    def downsample(data, mult):
        """Given 1D data, return the binned average."""
        overhang = len(data) % mult
        if overhang:
            data = data[:-overhang]
        data = numpy.reshape(data, (len(data) / mult, mult))
        data = numpy.average(data, 1)
        return data

    # TODO: This is the next method I need to look at, after the clean up and also after the put it in a good position.
    def get_frequency_power(self, data, trim=10, ys_divisor=100):
        flattened_data = data.flatten()
        left, right = numpy.split(numpy.abs(numpy.fft.fft(flattened_data)), 2)
        ys = numpy.add(left, right[::-1])
        ys = numpy.multiply(20, numpy.log10(ys))
        xs = numpy.arange(self.buffer_size / 2, dtype=float)
        #if trim:
            #i = int((self.buffer_size / 2) / trim)
            #ys = ys[:i]
            #xs = xs[:i] * self.rate / self.buffer_size
        if ys_divisor:
            ys /= float(ys_divisor)
        return xs, ys

    def get_furier(frequency, power):
        power *= float(100)#ys_divisor


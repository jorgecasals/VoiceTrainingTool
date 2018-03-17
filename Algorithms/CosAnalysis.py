import math
import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")
import numpy

class CosAnalysis:
    def __init__(self):
        self.t0 = 50
        self.T = 100
        self.nSample = 2001
        self.t = list(numpy.linspace(self.t0, self.t0+self.T, self.nSample))
        self.A = [10 , 5];
        w_factor = 2.0 * math.pi / 100.0
        self.w = [100.0 * w_factor, 200.0 * w_factor]
        self.phi = [math.pi / 3, math.pi / 2]
        self.y = []
        self.fft_y = []

    def print_cos_function_furier_transformation(self):

        plt.interactive(True)

        self.generate_signal()
        self.plot(self.t, self.y)

        self.transform_signal()

        self.reconstruct_signal()

        self.filter_signal(150)

        plt.interactive(True)

    def filter_signal(self, borders):
        self.fft_y_filtered = [0] * len(self.fft_y)

        for i in range(0, len(self.fft_y)):
            if i > borders and i < len(self.fft_y_filtered) - borders:
                self.fft_y_filtered[i] = self.fft_y[i]
            else:
                self.fft_y_filtered[i] = 0

        plt.figure(2)
        plt.subplot(2, 1, 2)
        power_spectrum_filtered = map(lambda x: math.pow(math.fabs(x), 2), self.fft_y_filtered)
        plt.plot(power_spectrum_filtered)
        self.y_filtered = numpy.fft.ifft(self.fft_y_filtered)
        plt.figure(1)
        plt.subplot(2,1,2)
        plt.plot(self.t, self.y_filtered)

    def reconstruct_signal(self):
        self.y_reconstructed = numpy.fft.ifft(self.fft_y, len(self.fft_y))
        plt.figure(3)
        plt.plot(self.t, self.y, self.t, self.y_reconstructed)
        plt.legend('original', 'reconstructed')
        plt.figure(4)
        plt.plot(self.y, self.y_reconstructed)

    def transform_signal(self):
        self.fft_y = numpy.fft.fft(self.y, len(self.y))
        plt.figure(2)
        plt.subplot(2,1,1)
        power_spectrum = map(lambda x: math.pow(math.fabs(x), 2), self.fft_y)
        plt.plot(power_spectrum)


    def generate_signal(self):
        self.y = [0] * len(self.t)
        for i in range(0, len(self.w)):
            new_values = map(lambda x: self.A[i]* math.cos(self.w[i]*x + self.phi[i]), self.t)
            self.y = [a + b for a, b in zip(self.y, new_values)]


    def plot(self, abcise, signal):
        plt.figure(1)
        plt.subplot(2, 1, 1)
        plt.plot(abcise, signal)
import numpy
#this will be splitted into two classes with main responsabilities:
# 1) transform audio in furier(interface with numpy) and viceversa
# 2) manipulate the audio transformed data.
from Logger import Logger


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
    def get_frequency_power2(self, data, trim=10, ys_divisor=100):
        # flattened_data = data.flatten()
        audio_frame_int = numpy.fromstring(data, dtype=numpy.int16)
        left, right = numpy.split(numpy.abs(numpy.fft.fft(audio_frame_int)), 2)
        power = numpy.add(left, right[::-1])
        power = power * len(data)
        # power = numpy.multiply(20, numpy.log10(power))
        frequencies = numpy.arange(self.buffer_size / 2, dtype=float)
        #if trim:
            #i = int((self.buffer_size / 2) / trim)
            #ys = ys[:i]
            #xs = xs[:i] * self.rate / self.buffer_size
        #if ys_divisor:
        #    ys /= float(ys_divisor)
        return frequencies, power

    def levelup_frecuencies(self, start_frequencies, end_frequencies, power_percentage, audio):
        audio_leveled_up = []
        power_multiple = (100.0 + power_percentage)/100
        for audio_frame in audio:
            audio_int = numpy.fromstring(audio_frame, dtype=numpy.int16)
            frequencies_level = numpy.fft.rfft(audio_int)
            frequencies_level[start_frequencies:end_frequencies] *= power_multiple
            audio_complex = numpy.fft.irfft(frequencies_level)
            audio_float = numpy.real(audio_complex)
            audio_int = []
            for float_value in audio_float:
                audio_int.append(int(round(float_value)))
            audio_int16 = numpy.array(audio_int, dtype=numpy.int16)
            audio_string = audio_int16.tostring()
            audio_leveled_up.append(audio_string)
        return audio_leveled_up

    def get_frequency_power(self, wave_data):
        frequency_power = []
        # for audio_frame in wave_data:
        audio_frame_int = numpy.fromstring(wave_data, dtype=numpy.int16)
        values_transformed_by_furier = numpy.fft.fft(audio_frame_int)
        # frequency_power.append(values_transformed_by_furier)
        return values_transformed_by_furier


    @Logger.log_it
    def transform(self, values):
        # data = self.get_frequency_power(values)
        frequency, power = self.get_frequency_power2(values)
        return frequency, power


    def clone_higher_frecuencies(self, source_start, source_end, audio):
        audio_leveled_up = []
        for audio_frame in audio:
            audio_int = numpy.fromstring(audio_frame, dtype=numpy.int16)
            frequencies_level = numpy.fft.rfft(audio_int)
            audio_end = len(frequencies_level)
            elements_to_switch = audio_end - source_end
            new_end = source_start+elements_to_switch
            frequencies_level[source_end:audio_end] = frequencies_level[source_start:new_end]
            audio_complex = numpy.fft.irfft(frequencies_level)
            audio_float = numpy.real(audio_complex)
            audio_int = []
            for float_value in audio_float:
                audio_int.append(int(round(float_value)))
            audio_int16 = numpy.array(audio_int, dtype=numpy.int16)
            audio_string = audio_int16.tostring()
            audio_leveled_up.append(audio_string)
        return audio_leveled_up

    def convert_to_int16_array(self, audio):
        audio_int16_array = []
        for string_audio in audio:
            int_audio = numpy.fromstring(string_audio, dtype=numpy.int16)
            audio_int16_array.append(int_audio)
        return audio_int16_array

    def convert_to_string_array(self, audio_int16_array):
        audio_string_array = []
        for int16_audio in audio_int16_array:
            string_audio = int16_audio.tostring()
            audio_string_array.append(string_audio)
        return audio_string_array


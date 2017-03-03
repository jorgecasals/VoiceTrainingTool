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
        power = numpy.add(left, right[::-1])
        power = numpy.multiply(20, numpy.log10(power))
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

    def chunk(self, audio):
        data_unflatted = self.convert_to_int16_array(audio)
        numpy_data = numpy.empty_like(data_unflatted)
        numpy_data[:] = data_unflatted

        data_flatted = numpy_data.flatten()
        fft_data = numpy.fft.fft(data_flatted)
        recovered_data = numpy.fft.ifft(fft_data)
        real_recovered_data = numpy.real(recovered_data)
        audio_recovered = []
        index = 4096
        while index <= len(real_recovered_data):
            data_slice = real_recovered_data[index - 4096:index]
            int_data_slice = []
            for float_value in data_slice:
                int_data_slice.append(int(round(float_value)))
            int_numpy_data_slice = numpy.array(int_data_slice, dtype=numpy.int16)
            audio_recovered.append(int_numpy_data_slice)
            index += 4096

        audio_transformed_to_original = self.convert_to_string_array(audio_recovered)

    def convert_to_frequency_level_pair(self, audio):
        data = audio.flatten()
        left, right = numpy.split(numpy.abs(numpy.fft.fft(data)), 2)
        ys = numpy.add(left, right[::-1])
        ys = numpy.multiply(20, numpy.log10(ys))
        xs = numpy.arange(self.BUFFERSIZE / 2, dtype=float)
        # i = int((self.BUFFERSIZE / 2) / 10)
        # ys = ys[:i]
        # xs = xs[:i] * self.RATE / self.BUFFERSIZE
        ys = ys / float(100)
        return xs, ys

    def convert_to_audio(self, xs, ys):
        ys = ys*float(100)





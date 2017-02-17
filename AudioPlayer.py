import pyaudio
import numpy
from FurierTransformer import *


class MyPlayer:
    def __init__(self, recorder):
        self.recorder = recorder
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 48100
        self.RECORD_SECONDS = 5

    def play_sound(self):
        self.audio = self.recorder.audio
        self.pyaudio_instace = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.audio_stream = self.pyaudio_instace.open(format=self.FORMAT,
                                            channels=self.CHANNELS,
                                            rate=self.RATE,
                                            output=True,
                                            frames_per_buffer=self.CHUNK)
        for audio_chunk in self.audio:
            self.audio_stream.write(audio_chunk)

        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.pyaudio_instace.terminate()

    def play_sound_with_tff_transforming(self):
        self.audio = self.recorder.audio
        self.pyaudio_instace = pyaudio.PyAudio()
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48100
        audio_stream = self.pyaudio_instace.open(format=self.FORMAT,
                                            channels=self.CHANNELS,
                                            rate=self.RATE,
                                            output=True,
                                            frames_per_buffer=self.CHUNK)
        data_unflatted = self.convert_to_int16_array()
        numpy_data = numpy.empty_like(data_unflatted)
        numpy_data[:] = data_unflatted
        furier_transformer = FurierTransformer(self.CHUNK, 48100)
        frequency,power = furier_transformer.get_frequency_power(numpy_data)
        #alter the power of some ranges.
        fft_reconstructed_data = furier_transformer.get_furier(frequency, power)

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
        for audio_chunk in audio_transformed_to_original:
            audio_stream.write(audio_chunk)

        audio_stream.stop_stream()
        audio_stream.close()

        # close PyAudio
        self.pyaudio_instace.terminate()

    def convert_to_int16_array(self):
        audio_int16_array = []
        for string_audio in self.audio:
            int_audio = numpy.fromstring(string_audio, dtype=numpy.int16)
            audio_int16_array.append(int_audio)
        return audio_int16_array

    def convert_to_string_array(self, audio_int16_array):
        audio_string_array = []
        for int16_audio in audio_int16_array:
            string_audio = int16_audio.tostring()
            audio_string_array.append(string_audio)
        return audio_string_array



    #import numpy as np
    #import pylab as pl
    #rate, data = wavfile.read('FILE.wav')
    #t = np.arange(len(data[:, 0])) * 1.0 / rate
    #pl.plot(t, data[:, 0])
    #pl.show()


    #p = 20 * np.log10(np.abs(np.fft.rfft(data[:2048, 0])))
    #f = np.linspace(0, rate / 2.0, len(p))
    #pl.plot(f, p)
    #pl.xlabel("Frequency(Hz)")
    #pl.ylabel("Power(dB)")
    #pl.show()
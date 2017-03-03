import pyaudio
import numpy
from FurierTransformer import *

#TODO:Too much responsability, I'm going to move the fft to another class. This is just for reproduce purpose.
class MyPlayer:
    def __init__(self, recorder):
        self.recorder = recorder
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5

    def play_sound(self):
        self.audio = self.recorder.audio
        self.pyaudio_instace = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.play_audio(self.audio)



    def play_sound_with_some_frequencies_higher(self):
        self.audio = self.recorder.audio
        self.pyaudio_instace = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16

        furier_transformer = FurierTransformer(buffer_size=self.CHUNK, rate=self.RATE)
        new_audio = furier_transformer.levelup_frecuencies(start_frequencies=100, end_frequencies=200, power_percentage=1000, audio=self.audio)
        self.play_audio(new_audio)

    def play_sound_with_some_frequencies_cloned_to_higer_position(self):
        self.audio = self.recorder.audio
        self.pyaudio_instace = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16

        furier_transformer = FurierTransformer(buffer_size=self.CHUNK, rate=self.RATE)
        new_audio = furier_transformer.clone_higher_frecuencies(source_start=100, source_end=200, audio=self.audio)
        self.play_audio(new_audio)

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

    def play_audio(self, audio_to_play):
        my_audio_stream = self.pyaudio_instace.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                                      output=True, frames_per_buffer=self.CHUNK)
        for audio_chunk in audio_to_play:
            my_audio_stream.write(audio_chunk)

        my_audio_stream.stop_stream()
        my_audio_stream.close()
        self.pyaudio_instace.terminate()

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
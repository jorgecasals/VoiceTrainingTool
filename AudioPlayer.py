import pyaudio
import numpy


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
        RECORD_SECONDS = 5
        audio_stream = self.pyaudio_instace.open(format=self.FORMAT,
                                            channels=self.CHANNELS,
                                            rate=self.RATE,
                                            output=True,
                                            frames_per_buffer=self.CHUNK)
        data_unflatted = numpy.fromstring(self.recorder.audio, dtype=numpy.int16)
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

        # audio_transformed_to_original = numpy.from
        for audio_chunk in audio_recovered:
            audio_stream.write(audio_chunk)

        audio_stream.stop_stream()
        audio_stream.close()

        # close PyAudio
        self.pyaudio_instace.terminate()

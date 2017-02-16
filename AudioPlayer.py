import pyaudio
import numpy


class MyPlayer:
    ##TODO:First change into the class. We need some clean up here.
    def __init__(self, recorder):
        self.recorder = recorder

    def play_sound(self):
        audio = self.recorder.audio
        pyaudio_instace = pyaudio.PyAudio()
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 48100
        RECORD_SECONDS = 5
        audio_stream = pyaudio_instace.open(format=FORMAT,
                                            channels=CHANNELS,
                                            rate=RATE,
                                            output=True,
                                            frames_per_buffer=CHUNK)
        start_stream_index = 0
        end_stream_index = CHUNK
        audio_lenght = len(audio)
        ##TODO: If there is a remainer part lower than a chunk it will not be played.
        for audio_chunk in audio:
            audio_stream.write(audio_chunk)
            # start_stream_index += CHUNK
            # end_stream_index += CHUNK

        audio_stream.stop_stream()
        audio_stream.close()

        # close PyAudio
        pyaudio_instace.terminate()

    def play_sound_with_tff_transforming(self):
        audio = self.recorder.audio
        pyaudio_instace = pyaudio.PyAudio()
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 48100
        RECORD_SECONDS = 5
        audio_stream = pyaudio_instace.open(format=FORMAT,
                                            channels=CHANNELS,
                                            rate=RATE,
                                            output=True,
                                            frames_per_buffer=CHUNK)
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
            for d in data_slice:
                int_data_slice.append(int(round(d)))
            int_numpy_data_slice = numpy.array(int_data_slice, dtype=numpy.int16)
            audio_recovered.append(int_numpy_data_slice)
            index += 4096

        ##TODO: If there is a remainer part lower than a chunk it will not be played.
        ##audio_transformed_to_original = numpy.from
        for audio_chunk in audio_recovered:
            audio_stream.write(audio_chunk)

        audio_stream.stop_stream()
        audio_stream.close()

        # close PyAudio
        pyaudio_instace.terminate()

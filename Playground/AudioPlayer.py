import pyaudio
from Logger import Logger

#TODO:Too much responsability, I'm going to move the fft to another class. This is just for reproduce purpose.
class AudioPlayer:

    def __init__(self, time_max = 30):
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = time_max
        self.name = "Audio Player"

    def play_sound_from_data(self, data):
        self.pyaudio_instace = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.play_audio(data)

    def play_audio(self, audio_to_play):
        Logger.info(self, "Audio playing started")
        my_audio_stream = self.pyaudio_instace.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                                      output=True, frames_per_buffer=self.CHUNK)
        for audio_chunk in audio_to_play:
            my_audio_stream.write(audio_chunk)

        my_audio_stream.stop_stream()
        my_audio_stream.close()
        self.pyaudio_instace.terminate()
        Logger.info(self, "Audio playing finalized")

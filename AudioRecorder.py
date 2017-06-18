import struct

import matplotlib
from scipy.io import wavfile

matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!
import numpy
import pyaudio
import threading
import time
from Logger import Logger
import wave

class AudioRecorder:
    def __init__(self, recording_time = 5):
        self.newAudio = False
        self.RATE = 44100
        self.BUFFER_SIZE = 1024 #= 2 ** 12
        self.reading_size = 1024*8
        self.audio = []
        self.py_audio = pyaudio.PyAudio()
        self.sound_card = self.py_audio.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                                             frames_per_buffer=self.BUFFER_SIZE)
        self.recording_is_stopped = True
        self.recording_time = recording_time
        self.name = "Audio Recorder"
        self.path = "D:\Person\VoiceTrainingTool\Tests\Resources\demo.wav"


    def release_sound_card(self):
        self.py_audio.close(self.sound_card)

    def get_audio_with_buffer_size(self):
        audio_string = self.sound_card.read(self.reading_size)

        return audio_string

    def record(self):
        self.recording_thread = threading.Thread(target=self.record_in_new_thread)
        self.recording_thread.start()
        #TODO UX: Show message to the user saying that thread should not be started when there another one running.

    @Logger.log_it
    def record_in_new_thread(self):
        Logger.info(self, "Audio Recording started")
        end_time = time.time() + self.recording_time
        self.audio = []
        self.recording_is_stopped = False
        while end_time > time.time():
            if self.recording_is_stopped:
                break
            self.audio.append(self.get_audio_with_buffer_size())
            self.newAudio = True
        Logger.info(self, "Audio Recording finalized")

    def stop_recording(self):
        self.recording_is_stopped = True

    def save_recording(self):
        try:
            Logger.info(self, "creating file with audio recorded")

            audio_file = wave.open(self.path, 'w')
            audio_file.setnchannels(1)
            sample_size = self.py_audio.get_sample_size(pyaudio.paInt16)
            audio_file.setsampwidth(sample_size)
            audio_file.setframerate(self.RATE)
            for buffer in self.audio:
                audio_file.writeframes(buffer)
            audio_file.close()

            Logger.info(self, "saved file")
        except Exception, e:
            Logger.error(self, str(e))

    @Logger.log_it
    def read_recording(self):
        try:
            audio_file = wave.open(self.path, 'r')
            data = []
            frames = audio_file.readframes(self.reading_size)
            while len(frames) > 0:
                data.append(frames)
                frames = audio_file.readframes(self.reading_size)


            Logger.info(self, "audio readed from file successfully")
            self.audio = data
            self.newAudio = True
            return data

        except Exception, e:
            Logger.error(self, str(e))

            #Logger.info(self, "reading audio from file saved")
            #samplerate, data = wavfile.read(self.path)
            #times = numpy.arange(len(data)) / float(samplerate)

            #i = 0
            #list_of_lists = []#

            #while i < len(data):
            #    list_of_lists.append(data[i:i + samplerate])
            #    i += samplerate







#import matplotlib
#matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!
import numpy
import pyaudio
import threading
import time


class AudioRecorder:
    def __init__(self, recording_time):
        self.newAudio = False
        self.RATE = 48100
        self.BUFFER_SIZE = 1024 #= 2 ** 12
        self.secToRecord = .1
        self.audio = []
        self.py_audio = pyaudio.PyAudio()
        self.sound_card = self.py_audio.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                                             frames_per_buffer=self.BUFFER_SIZE)
        self.recording_is_stopped = True
        self.recording_time = recording_time

    def release_sound_card(self):
        self.py_audio.close(self.sound_card)

    def get_audio_with_buffer_size(self):
        audio_string = self.sound_card.read(self.BUFFER_SIZE)
        return audio_string

    def record(self):
        self.recording_thread = threading.Thread(target=self.record_in_new_thread)
        self.recording_thread.start()
        #TODO UX: Show message to the user saying that thread should not be started when there another one running.

    def record_in_new_thread(self):
        end_time = time.time() + self.recording_time
        self.audio = []
        self.recording_is_stopped = False
        while end_time > time.time():
            if self.recording_is_stopped:
                break
            self.audio.append(self.get_audio_with_buffer_size())
            self.newAudio = True
        print("end of record")

    def stop_recording(self):
        self.recording_is_stopped = True



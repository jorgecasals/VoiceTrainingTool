import matplotlib
matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!
import numpy
import pyaudio
import threading
import time
from Logger import Logger
import wave

class AudioRecorder:
    def __init__(self, recording_time):
        self.newAudio = False
        self.RATE = 44100
        self.BUFFER_SIZE = 1024 #= 2 ** 12
        self.secToRecord = .1
        self.audio = []
        self.py_audio = pyaudio.PyAudio()
        self.sound_card = self.py_audio.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                                             frames_per_buffer=self.BUFFER_SIZE)
        self.recording_is_stopped = True
        self.recording_time = recording_time
        self.name = "Audio Recorder"


    def release_sound_card(self):
        self.py_audio.close(self.sound_card)

    def get_audio_with_buffer_size(self):
        audio_string = self.sound_card.read(1024*8)

        return audio_string

    def record(self):
        self.recording_thread = threading.Thread(target=self.record_in_new_thread)
        self.recording_thread.start()
        #TODO UX: Show message to the user saying that thread should not be started when there another one running.

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
            path = "D:\Person\VoiceTrainingTool\demo.wav"
            wf = wave.open(path, 'w')
            wf.setnchannels(1)
            sample_size = self.py_audio.get_sample_size(pyaudio.paInt16)
            wf.setsampwidth(sample_size)
            wf.setframerate(self.RATE)
            for buffer in self.audio:
                wf.writeframes(buffer)
            wf.close()
            Logger.info(self, "saved file")
        except Exception, e:
            Logger.error(self, str(e))





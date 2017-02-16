import matplotlib

matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!
import numpy
import pyaudio
import threading
import time


class MyRecorder:
    """Simple, cross-platform class to record from the microphone."""

    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE = 48100
        self.BUFFERSIZE = 2 ** 12  # 1024 is a good buffer size
        self.secToRecord = .1
        self.threadsDieNow = False
        self.newAudio = False
        self.setup()


    def setup(self):
        """initialize sound card."""
        # TODO - windows detection vs. alsa or something for linux
        # TODO - try/except for sound card selection/initiation

        self.buffersToRecord = int(self.RATE * self.secToRecord / self.BUFFERSIZE)
        if self.buffersToRecord == 0:
            self.buffersToRecord = 1
        self.samplesToRecord = int(self.BUFFERSIZE * self.buffersToRecord)
        self.chunksToRecord = int(self.samplesToRecord / self.BUFFERSIZE)
        self.secondsPerPoint = 1.0 / self.RATE

        self.pyAudio = pyaudio.PyAudio()
        self.sound_card = self.pyAudio.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                                            frames_per_buffer=self.BUFFERSIZE)
        ### TODO Jorge: Borrar las variables que no se usan para nada.
        self.xsBuffer = numpy.arange(self.BUFFERSIZE) * self.secondsPerPoint
        self.xs = numpy.arange(self.chunksToRecord * self.BUFFERSIZE) * self.secondsPerPoint
        self.audio = []

    def release_sound_card(self):
        """cleanly back out and release sound card."""
        self.pyAudio.close(self.sound_card)

    ### RECORDING AUDIO ###

    def get_audio(self):
        """get a single buffer size worth of audio."""
        audio_string = self.sound_card.read(self.BUFFERSIZE)
        return audio_string
        ##return numpy.fromstring(audio_string, dtype=numpy.int16)

    def record(self):
        self.t = threading.Thread(target=self.record_in_new_thread)
        self.t.start()


    def record_in_new_thread(self):
        """record secToRecord seconds of audio."""
        end_time = time.time() + 5
        self.audio = []
        while end_time > time.time():
            if self.threadsDieNow:
                break
            self.audio.append(self.get_audio())
            self.newAudio = True
        print("end of record")

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow = True

    ### MATH ###

    def downsample(self, data, mult):
        """Given 1D data, return the binned average."""
        overhang = len(data) % mult
        if overhang:
            data = data[:-overhang]
        data = numpy.reshape(data, (len(data) / mult, mult))
        data = numpy.average(data, 1)
        return data
# This is the next method I need to look at, after the clean up and also after the put it in a good position.
    def fft(self, data=None, trimBy=10, logScale=False, divBy=100):
        if data == None:
            data = self.audio.flatten()
        left, right = numpy.split(numpy.abs(numpy.fft.fft(data)), 2)
        ys = numpy.add(left, right[::-1])
        if logScale:
            ys = numpy.multiply(20, numpy.log10(ys))
        xs = numpy.arange(self.BUFFERSIZE / 2, dtype=float)
        if trimBy:
            i = int((self.BUFFERSIZE / 2) / trimBy)
            ys = ys[:i]
            xs = xs[:i] * self.RATE / self.BUFFERSIZE
        if divBy:
            ys = ys / float(divBy)
        return xs, ys


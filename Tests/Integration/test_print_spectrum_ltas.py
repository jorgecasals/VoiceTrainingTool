from AudioRecorder import AudioRecorder
from Entities.Audio import Audio
import numpy
from Algorithms.SpectrumCreator import SpectrumCreator
from Algorithms.LtasCreator import LtasCreator

import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")


def test_print_bababa_spectrum():
    plt.interactive(True)
    string_frames_audio = read_data_from_file_demo()
    byte_frames_audio = numpy.fromstring(string_frames_audio, dtype=numpy.int16)
    audio = Audio(byte_frames_audio)
    spectrum = SpectrumCreator().create_spectrum_from_audio(audio)
    plt.plot(spectrum.frequencies, spectrum.get_absolute_values())
    plt.interactive(True)

def test_print_bababa_ltas():
    plt.interactive(True)
    string_frames_audio = read_data_from_file_demo()
    byte_frames_audio = numpy.fromstring(string_frames_audio, dtype=numpy.int16)
    audio = Audio(byte_frames_audio)
    spectrum = SpectrumCreator().create_spectrum_from_audio(audio)
    ltas = LtasCreator().create_ltas_from_spectrum(spectrum)

    plt.plot(ltas.bands, ltas.values)
    plt.interactive(True)

def get_audio_frames():
    string_frames_audio = read_data_from_file_demo()
    byte_frames_audio = numpy.fromstring(string_frames_audio, dtype=numpy.int16)
    return byte_frames_audio


def read_data_from_file_demo():
    recorder = AudioRecorder()
    recorded = recorder.read_recording()
    data_total = ''
    for data in recorded:
        data_total += data

    return data_total





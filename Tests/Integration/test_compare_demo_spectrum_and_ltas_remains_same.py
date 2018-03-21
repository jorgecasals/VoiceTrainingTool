from Entities.Audio import Audio
import numpy
from BababaConstants import BABABA_SPECTRUM_VALUES_PATH
from BababaConstants import BABABA_LTAS_VALUES_PATH
from Algorithms.SpectrumCreator import SpectrumCreator
from Algorithms.LtasCreator import LtasCreator
from AudioRecorder import AudioRecorder

def test_bababa_ltas_values_remains_the_same():
    audio_frames = get_audio_frames()
    audio = Audio(audio_frames)
    spectrum = SpectrumCreator().create_spectrum_from_audio(audio)
    ltas = LtasCreator().create_ltas_from_spectrum(spectrum)
    saved_ltas_values = get_list_values(BABABA_LTAS_VALUES_PATH)
    ltas_remains_the_same = compare_lists(ltas.values, saved_ltas_values)
    assert ltas_remains_the_same

def test_bababa_spectrum_values_remains_the_same():
    audio_frames = get_audio_frames()
    audio = Audio(audio_frames)
    spectrum = SpectrumCreator().create_spectrum_from_audio(audio)
    saved_spectrum_values = get_list_values(BABABA_SPECTRUM_VALUES_PATH)
    spectrum_remains_the_same = compare_lists(spectrum.values, saved_spectrum_values)
    assert spectrum_remains_the_same

def get_list_values(path):
    file_with_list_values = open(path, 'r')
    values = file_with_list_values.read().splitlines()
    file_with_list_values.close()
    return values

def compare_lists(new_values, expected_values):
    new_values_len = len(new_values)
    if new_values_len != len(expected_values): return False
    for index in range(0, new_values_len):
        new_value = new_values[index]
        expected_value = expected_values[index]
        if str(new_value) != str(expected_value):
            return False
    return True

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
from AudioRecorder import AudioRecorder
from Entities.Audio import Audio
import numpy
from BababaConstants import BABABA_SPECTRUM_VALUES_PATH
from BababaConstants import BABABA_LTAS_VALUES_PATH
from Algorithms.SpectrumCreator import SpectrumCreator
from Algorithms.LtasCreator import LtasCreator
import numpy
from AudioRecorder import AudioRecorder

from Algorithms.LtasCreator import LtasCreator
from Algorithms.SpectrumCreator import SpectrumCreator
from BababaConstants import BABABA_LTAS_VALUES_PATH
from BababaConstants import BABABA_SPECTRUM_VALUES_PATH
from Entities.Audio import Audio


def test_save_ltas_spectrum_values_from_bababa_file():
    audio_frames = get_audio_frames()
    audio = Audio(audio_frames)
    spectrum = SpectrumCreator.create_spectrum_from_audio(audio)
    save_list_values(BABABA_SPECTRUM_VALUES_PATH, spectrum.values)
    ltas = LtasCreator().create_ltas_from_spectrum(spectrum)
    save_list_values(BABABA_LTAS_VALUES_PATH, ltas.values)

def save_list_values(path, list):
    file_with_list_values = open(path, 'w')
    for item in list:
        file_with_list_values.write("%s\n" % item)

    file_with_list_values.close()

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

from datetime import datetime

import pytest

from Entities.VoiceSound import VoiceSound

from SoundAnalyzer import SoundAnalyzer
from Sound import Sound
from AudioRecorder import AudioRecorder
import Constants as const
from Spectrum import Spectrum


def test_sound_to_spectrum_with_null_values_raise_exception():
    analyzer = SoundAnalyzer()
    spectrum = analyzer.sound_to_spectrum(sound=None, fast=None)
    assert spectrum is None


def peek_data_from_file_demo():
    recorder = AudioRecorder()
    recording_data = recorder.read_recording()
    return recording_data


def test_pass_demo_file_to_sound_to_spectrum():
    data = peek_data_from_file_demo()
    sound = VoiceSound(data, "Author", datetime.now())
    spectrum = sound.BuildSpectrum()
    print(spectrum)
    # sound = Sound(audio_data=data, number_of_channels=1, start_time=0, end_time=5, number_of_samples=len(data), sampling_period=None, time_of_first_sample=0)
    # spectrum = Spectrum(sound, highest_frequency=20000, number_of_frequencies=20000)
    # print(spectrum)

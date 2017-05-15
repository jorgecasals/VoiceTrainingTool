import pytest
from SoundAnalyzer import SoundAnalyzer
from Sound import Sound

def test_sound_to_spectrum_with_null_values_raise_exception():
    analyzer = SoundAnalyzer()
    spectrum = analyzer.sound_to_spectrum(sound=None, fast=None)
    assert spectrum is None

def peek_data_from_file_demo():
    return None

def test_pass_demo_file_to_sound_to_spectrum():
    analyzer = SoundAnalyzer()
    data = peek_data_from_file_demo()
    sound = Sound(audio_data = data, number_of_channels=1, start_time=0, end_time=5, number_of_samples=None, samplin_period=None, time_of_first_sample=None)
    analyzer = SoundAnalyzer()
    analyzer.sound_to_spectrum(sound=sound, fast=False)
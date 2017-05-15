import pytest
from SoundAnalyzer import SoundAnalyzer
from AudioRecorder import AudioRecorder

def test_sound_to_spectrum_with_null_values_raise_exception():
    analyzer = SoundAnalyzer()
    spectrum = analyzer.sound_to_spectrum(sound=None, fast=None)
    assert spectrum is None


def test_creating_a_file():
    recorder = AudioRecorder(5)
    recorder.save_recording('x', 'y')
from datetime import datetime

import pytest

from Entities.VoiceSound import VoiceSound
from Algorithms import CosAnalysis

from SoundAnalyzer import SoundAnalyzer
from Sound import Sound
from AudioRecorder import AudioRecorder
#import Constants as const


def test_cos():
    analysis = CosAnalysis.CosAnalysis()
    analysis.print_cos_function_furier_transformation()

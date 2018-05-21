from DataManagement.PathBuilders import *
from Repositories.TrainingDataRepository import TrainingDataRepository
from Entities.Spectrum import Spectrum


class SpectrumRepository(TrainingDataRepository):
    def __init__(self):
        TrainingDataRepository.__init__(self, SpectrumPathBuilder, Spectrum)

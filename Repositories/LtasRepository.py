from DataManagement.PathBuilders import *
from Repositories.TrainingDataRepository import TrainingDataRepository
from Entities.Ltas import Ltas


class LtasRepository(TrainingDataRepository):
    def __init__(self):
        TrainingDataRepository.__init__(self, LtasPathBuilder, Ltas)
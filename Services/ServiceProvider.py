from Services.UserService import UserService
from Services.TrainingService import TrainingService
from Services.LtasService import LtasService
from Services.SpectrumService import SpectrumService

from Repositories.RepositoryProvider import *


user_service = UserService(user_repository, training_repository)

training_service = TrainingService(training_repository, user_repository, lecture_repository, sound_repository)

ltas_service = LtasService(ltas_repository, sound_repository)

spectrum_service = SpectrumService(spectrum_repository, sound_repository)
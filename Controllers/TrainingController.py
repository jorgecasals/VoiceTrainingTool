import sys

from PyQt4.QtGui import QTableView
from Algorithms.ProjectionCalculator import ProjectionCalculator
from Algorithms.SoundAlgorithms import SoundAlgorithms
import ViewsNavigator
import Services.ServiceProvider
import Session
from UI.Models.TableColumnModel import TableColumnModel
from UI.Models.TableModel import TableModel, QHeaderView, QAbstractItemView
from PyQt4.QtGui import *

from PyQt4 import QtCore, QtGui,uic
from AudioPlayer import AudioPlayer

class TrainingController (QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(TrainingController, self).__init__(parent)
        self.training_service = Services.ServiceProvider.training_service
        self.ltas_service = Services.ServiceProvider.ltas_service
        self.spectrum_service = Services.ServiceProvider.spectrum_service
        self.player = AudioPlayer()

        uic.loadUi('..\UI\\training.ui', self)
        self.register_buttons_actions()
        self.load_data()
        self.configureMenus()
        self.show()

    def register_buttons_actions(self):
        self.training_btn_start.clicked.connect(self.click_start)
        self.training_btn_logout.clicked.connect(self.click_logout)
        self.training_btn_stats.clicked.connect(self.click_stats)

    def load_data(self):
        self.load_previous_trainings()
        self.load_readings()

    def load_previous_trainings(self):
        previous_trainings = self.training_service.get_previous_training_of_user(Session.user_name)
        projection_level_for_trainings_dict = self.get_projection_level_for_trainings_dict(previous_trainings)

        header = [
             TableColumnModel(name='Number', get_data_func=lambda x: x.number)
            ,TableColumnModel(name='Date',get_data_func=lambda x: x.creation_date)
            ,TableColumnModel(name='Reading',get_data_func=lambda x: x.reading_title)
            , TableColumnModel(name='Recording time', get_data_func=lambda x: x.time_dedicated)
            , TableColumnModel(name='projection_level', get_data_func=lambda x: projection_level_for_trainings_dict[x])
        ]

        myModel = TableModel(self, previous_trainings, header)
        self.training_tbl_previous_trainings.setModel(myModel)

    def get_projection_level_for_trainings_dict(self, previous_trainings):
        trainings_ltas_dict = {}
        ltas_list = []
        for training in previous_trainings:
            ltas = self.ltas_service.get_ltas(Session.user_name, training.number)
            trainings_ltas_dict[training] = ltas
            ltas_list.append(ltas)
        min_ltas_value = min(map(lambda t: t.get_min_value(), ltas_list))
        for training in previous_trainings:
            trainings_ltas_dict[training] = trainings_ltas_dict[training].get_ltas_normalized(min_ltas_value)

        training_projection_level_dict = {}
        for training in previous_trainings:
            ltas = trainings_ltas_dict[training]
            projection_level = ProjectionCalculator().measure_projection(ltas=ltas)
            training_projection_level_dict[training] = projection_level

        return training_projection_level_dict

    def get_projection_level(self, sound):
        ltas = SoundAlgorithms().calculate_ltas_from_sound(sound)
        projection_level = ProjectionCalculator().measure_projection(ltas=ltas)
        return projection_level

    def load_readings(self):
        self.available_readings = self.training_service.get_readings_for_training()
        self.training_cmb_readings.clear()
        titles = map(lambda r: r.title, self.available_readings)
        self.training_cmb_readings.addItems(titles)

    def click_start(self):
        selected_reading_title = str(self.training_cmb_readings.currentText())
        Session.selected_reading = selected_reading_title
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.trainer)

    def click_logout(self):
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.login)

    def click_stats(self):
        pass
        #ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.login)

    def click_cancel(self):
        self.close()

    def showEvent(self, *args, **kwargs):
        self.load_data()
        header = self.training_tbl_previous_trainings.horizontalHeader()
        header.setResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def click_register(self):
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.register)

    def convert_selected_to_ltas(self):
        selected_row = self.training_tbl_previous_trainings.selectionModel().currentIndex().row()
        selected_value = self.training_tbl_previous_trainings.model().data_list[selected_row]
        print(selected_value)
        self.ltas_service.create_ltas(selected_value.user_name, selected_value.number)
        print("ltas created")

    def convert_selected_to_spectrum(self):
        selected_row = self.training_tbl_previous_trainings.selectionModel().currentIndex().row()
        selected_value = self.training_tbl_previous_trainings.model().data_list[selected_row]
        self.spectrum_service.create_spectrum(selected_value.user_name, selected_value.number)
        print("spectrum created")

    def play_sound_of_selected_training(self):
        selected_row = self.training_tbl_previous_trainings.selectionModel().currentIndex().row()
        selected_value = self.training_tbl_previous_trainings.model().data_list[selected_row]
        sound = self.training_service.get_sound_of_training(selected_value.user_name, selected_value.number)
        self.player.play_sound_from_data(sound)
        print("playing the sound of the selected training")

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        to_ltas_action = menu.addAction("To Ltas")
        to_spectrum_action = menu.addAction("To Spectrum")
        play_sound_action = menu.addAction("Play sound")
        action = menu.exec_(event.globalPos())
        if action == to_ltas_action:
            self.convert_selected_to_ltas()
        elif action == to_spectrum_action:
            self.convert_selected_to_spectrum()
        elif action == play_sound_action:
            self.play_sound_of_selected_training()


    def configureMenus(self):
        self.training_tbl_previous_trainings.setSelectionBehavior(QAbstractItemView.SelectRows)
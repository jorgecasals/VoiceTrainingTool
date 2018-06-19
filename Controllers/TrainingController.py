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
from Algorithms.SoundAlgorithms import SoundAlgorithms
from Controllers.PlotController import PlotController
from datetime import datetime

from PyQt4 import QtCore, QtGui,uic
from Playground.AudioPlayer import AudioPlayer

class TrainingController (QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(TrainingController, self).__init__(parent)
        self.training_service = Services.ServiceProvider.training_service
        self.ltas_service = Services.ServiceProvider.ltas_service
        self.spectrum_service = Services.ServiceProvider.spectrum_service
        self.player = AudioPlayer()
        self.sound_algoritms = SoundAlgorithms()
        uic.loadUi('..\UI\\training.ui', self)
        self.configure_plots()
        self.register_buttons_actions()
        self.load_data()
        self.configureMenus()
        self.listen_to_selection_changed()
        self.just_init_was_called = True
        self.show()

    def register_buttons_actions(self):
        self.training_btn_start.clicked.connect(self.click_start)
        self.training_btn_logout.clicked.connect(self.click_logout)

    def load_data(self):
        self.load_previous_trainings_data_in_controls()
        self.load_readings()

    def reload_data(self):
        self.delete_plots()
        self.delete_historic_plot()
        self.configure_plots()
        self.load_previous_trainings_data_in_controls()
        self.listen_to_selection_changed()
        self.load_readings()

    def configure_plots(self):
        self.spectrum_plot = PlotController()
        self.plot_layout.addWidget(self.spectrum_plot)
        self.spectrum_plot.show()
        self.ltas_plot = PlotController(abs_units='kHz', y_label='Amplitude', coord_units='dB')
        self.plot_layout.addWidget(self.ltas_plot)
        self.ltas_plot.show()
        self.historics_plot = PlotController(x_label='Training Number', y_label = 'Projection Level', abs_units='Int', coord_units='PL')
        self.historics_plot_layout.addWidget(self.historics_plot)
        self.historics_plot.show()

    def reset_selection_plots(self, spectrum, ltas):
        self.delete_plots()
        self.reset_spectrum_plot(spectrum.frequencies, spectrum.values)
        self.reset_ltas_plot(ltas.bands, ltas.values)

    def delete_plots(self):
        self.ltas_plot.setParent(None)
        self.spectrum_plot.setParent(None)

    def delete_historic_plot(self):
        self.historics_plot.setParent(None)

    def reset_ltas_plot(self, bands, data):
        self.ltas_plot = PlotController(abs_units='kHz')
        self.plot_layout.addWidget(self.ltas_plot)
        self.ltas_plot.update(bands, data)
        self.ltas_plot.show()

    def reset_spectrum_plot(self, frequencies, data):
        self.spectrum_plot = PlotController()
        self.plot_layout.addWidget(self.spectrum_plot)
        abs_data = abs(data)
        self.spectrum_plot.update_spectrum(abs_data)
        self.spectrum_plot.show()

    def listen_to_selection_changed(self):
        self.training_tbl_previous_trainings.connect(self.training_tbl_previous_trainings.selectionModel(),
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.selection_changed_event)
        #selection_model = self.training_tbl_previous_trainings.selectionModel()
        #selection_model.selectionChanged.connect(self.selection_changed_event)

    def load_previous_trainings_data_in_controls(self):
        projection_level_for_trainings_dict = self.load_previous_training_projection_level()
        self.update_previous_trainings_table(projection_level_for_trainings_dict)
        self.update_historics_plot(projection_level_for_trainings_dict)

    def update_historics_plot(self, projection_level_for_trainings_dict):

        trainings = projection_level_for_trainings_dict.keys()

        trainings.sort(key = lambda t: t.number)

        training_numbers = [training.number - 1 for training in trainings]

        projection_levels = [projection_level_for_trainings_dict[training] for training in trainings]

        self.historics_plot.update(training_numbers, projection_levels)

    def update_previous_trainings_table(self, projection_level_for_trainings_dict):
        (header, data) = self.build_previous_training_table_model(projection_level_for_trainings_dict)
        self.previous_trainings_model = TableModel(self, data, header)
        self.training_tbl_previous_trainings.setModel(self.previous_trainings_model)

    def load_previous_training_projection_level(self):
        projection_level_for_trainings_dict = {}
        previous_trainings = self.training_service.get_previous_training_of_user(Session.user_name)
        if previous_trainings != None and len(previous_trainings) > 0:
            projection_level_for_trainings_dict = self.get_projection_level_for_trainings_dict(previous_trainings)

        return projection_level_for_trainings_dict

    def build_previous_training_table_model(self, projection_level_for_trainings_dict):

        header = [
            TableColumnModel(name='Number', get_data_func=lambda x: x.number)
            , TableColumnModel(name='Date', get_data_func=lambda x: x.creation_date)
            , TableColumnModel(name='Reading', get_data_func=lambda x: x.reading_title)
            , TableColumnModel(name='Recording time', get_data_func=lambda x: x.time_dedicated)
            , TableColumnModel(name='projection_level', get_data_func=lambda x: projection_level_for_trainings_dict[x])]
        trainings = projection_level_for_trainings_dict.keys()

        return (header, trainings)

    def selection_changed_event(self, new, old):
        print("selection changed")
        selected_value = self.get_selected_value()
        sound = self.training_service.get_sound_of_training(selected_value.user_name, selected_value.number)
        spectrum = self.sound_algoritms.calculate_spectrum_from_sound(sound)
        ltas = self.sound_algoritms.calculate_ltas_from_spectrum(spectrum)
        self.reset_selection_plots(spectrum, ltas)

    def get_projection_level_for_trainings_dict(self, previous_trainings):
        trainings_ltas_dict = {}
        ltas_list = []
        for training in previous_trainings:
            sound = self.training_service.get_sound_of_training(Session.user_name, training.number)
            ltas = self.sound_algoritms.calculate_ltas_from_sound(sound)
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
        #ProjectionCalculator().normalize_projections(training_projection_level_dict, 5, 10)
        return training_projection_level_dict

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

    def click_cancel(self):
        self.close()

    def showEvent(self, *args, **kwargs):
        if self.just_init_was_called:
            self.just_init_was_called = False
        else:
            self.reload_data()
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

    def get_selected_value(self):
        selected_row = self.training_tbl_previous_trainings.selectionModel().currentIndex().row()
        selected_value = self.training_tbl_previous_trainings.model().data_list[selected_row]
        return selected_value

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        play_sound_action = menu.addAction("Play sound")
        action = menu.exec_(event.globalPos())
        if action == play_sound_action:
            self.play_sound_of_selected_training()


    def configureMenus(self):
        self.training_tbl_previous_trainings.setSelectionBehavior(QAbstractItemView.SelectRows)
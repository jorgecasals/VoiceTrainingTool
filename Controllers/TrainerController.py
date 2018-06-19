from PyQt4.QtGui import QPushButton

import ViewsNavigator
import Services.ServiceProvider
import Session
from Playground.AudioRecorder import AudioRecorder
import datetime
from Entities.Training import Training


from PyQt4 import QtCore, QtGui,uic

class TrainerController (QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(TrainerController, self).__init__(parent)
        self.training_service = Services.ServiceProvider.training_service
        self.ltas_service = Services.ServiceProvider.ltas_service
        self.audio_recorder = AudioRecorder()

        uic.loadUi('..\UI\\trainer.ui', self)
        self.register_buttons_actions()
        self.recording = False
        self.sound_recorded = ""
        self.set_no_ready_to_save_state()
        self.hide_recording_information()
        self.show()

    def register_buttons_actions(self):
        self.trainer_btn_record.clicked.connect(self.click_record_or_finish)
        self.trainer_btn_cancel.clicked.connect(self.click_cancel)
        self.trainer_btn_save.clicked.connect(self.click_save)

    def set_no_ready_to_save_state(self):
        self.training_lbl_save_text.hide()
        self.trainer_btn_save.hide()

    def set_ready_to_save_state(self):
        self.training_lbl_save_text.show()
        self.trainer_btn_save.show()

    def click_save(self):
        reading_title = Session.selected_reading
        readings = self.training_service.get_previous_training_of_user(Session.user_name)
        current_training = Training(number = len(readings) + 1, reading_title = reading_title, user_name = Session.user_name, time_dedicated = self.time_dedicated)
        self.training_service.create_training(current_training, self.sound_recorded)
        self.ltas_service.create_ltas(Session.user_name, current_training.number)
        self.go_back_to_trainings()

    def load_selected_reading(self):
        reading_title = Session.selected_reading
        select_reading = self.training_service.get_reading(reading_title)
        self.trainer_tb_text.setText(select_reading.text)

    def click_record_or_finish(self):
        if self.recording:
            self.trainer_btn_record.setText("Record again")
            self.set_ready_to_save_state()
            self.recording = False
            self.stop_recording()
        else:
            self.trainer_btn_record.setText("Finish")
            self.set_no_ready_to_save_state()
            self.recording = True
            self.start_recording()

    def click_cancel(self):
        self.go_back_to_trainings()

    def go_back_to_trainings(self):
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.trainings)

    def showEvent(self, *args, **kwargs):
        self.load_selected_reading()
        self.set_no_ready_to_save_state()
        self.trainer_btn_record.setText("Record")
        self.recording = False

    def hide_recording_information(self):
        self.training_lbl_recording.hide()
        self.training_lbl_recording_seconds.hide()
        self.recording_time_seconds = 0
        self.training_lbl_recording_seconds.setText(str(self.recording_time_seconds) + ' Seconds')

    def show_recording_information(self):
        self.training_lbl_recording.show()
        self.training_lbl_recording_seconds.show()
        self.looptimer = QtCore.QTimer()
        self.looptimer.timeout.connect(self.update_seconds)
        self.looptimer.start(1000)
        self.recording_time_seconds = 0

    def update_seconds(self):
        self.recording_time_seconds  = self.recording_time_seconds + 1
        self.training_lbl_recording_seconds.setText(str(self.recording_time_seconds) + ' Seconds')

    def start_recording(self):
        self.audio_recorder.record_in_new_thread()
        self.recording_starting_time = datetime.datetime.now()
        self.show_recording_information()

    def stop_recording(self):
        #get the data from the recorder
        self.audio_recorder.stop_recording()
        self.sound_recorded = self.audio_recorder.get_recording_in_memory()
        self.time_dedicated = str(datetime.datetime.now() - self.recording_starting_time)
        self.hide_recording_information()
        self.looptimer.stop()
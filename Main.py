import sys

from PyQt4 import QtCore, QtGui

import ui_plot
from AudioPlayer import *
from AudioRecorder import *
#TODO: Create local methods to call the player passing the time to playing and recording.
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    recorder = AudioRecorder(recording_time=5)
    player = MyPlayer(recorder)
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(recorder.record)
    uiplot.btnB.clicked.connect(player.play_sound)
    uiplot.btnC.clicked.connect(player.play_sound_with_some_frequencies_higher)
    uiplot.btnD.clicked.connect(player.play_sound_with_some_frequencies_cloned_to_higer_position)

    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)



    ### DISPLAY WINDOWS
    win_plot.show()
    code = app.exec_()
    sys.exit(code)

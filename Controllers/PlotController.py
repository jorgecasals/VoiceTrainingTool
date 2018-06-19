import numpy as np
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui
from Common.Constants import *
from UI.Models.PlotModel import PlotModel

class PlotController(pg.PlotWidget):

    read_collected = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, frequency_units='Hz'):
        super(PlotController, self).__init__()
        self.read_collected.connect(self.update)
        self.img = pg.ImageItem()
        self.addItem(self.img)

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-50,40])

        self.setLabel('bottom', 'Frequency', units=frequency_units)
        self.setLabel('left', 'Pascal', units='Pa')
        self.setWindowTitle('Training\'s spectrum')

    def update(self, data):
        # normalized, windowed frequencies in data chunk
        #spec = np.fft.rfft(chunk*self.win) / CHUNKSZ
        # get magnitude
        #psd = abs(spec)
        # convert to dB scale
        #psd = 20 * np.log10(psd)

        x_lenght = len(data)
        self.img_array = np.zeros(x_lenght)
        # setup the correct scaling for y-axis
        freq = np.arange((x_lenght/2)+1)/(float(x_lenght)/FS)
        yscale = 1.0/(self.img_array.shape[0]/freq[-1])
        self.img.scale((1./FS)*x_lenght, yscale)
        self.win = np.hanning(x_lenght)

        #psd = 20 * np.log10(psd)
        # roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)
        #self.img_array[-1:] = psd
        half_psd = data[0:len(freq)]
        self.plot(freq, half_psd)

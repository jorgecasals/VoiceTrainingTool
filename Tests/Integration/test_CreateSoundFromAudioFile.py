from datetime import datetime

import pytest

from Entities.VoiceSound import VoiceSound
from Entities.Spectrum import Spectrum
from Entities.SpectrumValue import SpectrumValue

from SoundAnalyzer import SoundAnalyzer
from Sound import Sound
from AudioRecorder import AudioRecorder
from Common.Constants import *
#import Constants as const
from Entities.Spectrum import Spectrum
from Entities.SpectrumValue import SpectrumValue
import numpy
from cmath import *
from math import ceil

import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")



def test_sound_to_spectrum_with_null_values_raise_exception():
    analyzer = SoundAnalyzer()
    spectrum = analyzer.sound_to_spectrum(sound=None, fast=None)
    assert spectrum is None


def read_data_from_file_demo():
    recorder = AudioRecorder()
    recorded = recorder.read_recording()
    data_total = ''
    for data in recorded:
        data_total += data

    return data_total


def test_sound_to_spectrum_passing_file():
    plt.interactive(True)
    string_frames_audio = read_data_from_file_demo()
    byte_frames_audio = numpy.fromstring(string_frames_audio, dtype=numpy.int16)
    (frequencies, intensity) = fft_harden(byte_frames_audio)
    plt.plot(frequencies, intensity)
    plt.interactive(True)

def test_sound_to_ltas_passing_file():
    plt.interactive(True)
    string_frames_audio = read_data_from_file_demo()
    byte_frames_audio = numpy.fromstring(string_frames_audio, dtype=numpy.int16)
    (spectrum_frequencies, spectrum_values, my_frequency_step) = convertir_spectrum(byte_frames_audio)
    ancho_banda = 1000.0
    (ltas_frequencies, ltas_values) = convertir_ltas(spectrum_frequencies, spectrum_values, ancho_banda,my_frequency_step)

    plt.plot(ltas_frequencies, ltas_values)
    plt.interactive(True)

def fft_myown(data, logScale=True):#, divBy=100):
    # left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
    # ys=numpy.add(left,right[::-1])
    ys = numpy.abs(numpy.fft.fft(data))
    if logScale:
        ys = numpy.array(numpy.multiply(20, numpy.log10(ys)))
    xs = build_frequencies_abcisa(ys)
    return xs, ys

    #xs = numpy.arange(len(data), dtype=float)
    #xs = xs * RATE / len(data)
    # furier_transformed_audio = numpy.fft.fft(byte_frames_audio)
    # spectrum = Spectrum()
    #first_spectrum_value = SpectrumValue(frequency=0, real=1, img=0)
    #spectrum.add_value(first_spectrum_value)
    #scale = sound_step = (1.0/44100.0)
     #= len(furier_transformed_audio)
    #frequency_step = 1.0 / (sound_step * sound_samples/2)
    #furier_transformed_audio_scaled = furier_transformed_audio * scale
    # position = 0
    # for complex_value in furier_transformed_audio:
    #     spectrum_value = SpectrumValue(frequency=position, real=numpy.real(complex_value), img=numpy.imag(complex_value))
    #     spectrum.add_value(spectrum_value)
    #     position += 1
    # print_spectrum(spectrum)
    # data = read_data_from_file_demo()
    # sound = VoiceSound(data, "Jorge", datetime.now())
    # spectrum = sound.build_spectrum()
    # print(spectrum.complex_values)
    # sound = Sound(audio_data=data, number_of_channels=1, start_time=0, end_time=5, number_of_samples=len(data), sampling_period=None, time_of_first_sample=0)
    # spectrum = Spectrum(sound, highest_frequency=20000, number_of_frequencies=20000)
    # print(spectrum)

#Creates an array with all the frequencies for which the intensity data has a value.
def build_frequencies_abcisa(intensity_data):
    frequency_step = (float(FREQUENCIES_TOTAL))/(float(len(intensity_data)))
    frequencies_abcisa = numpy.array(numpy.arange(0, FREQUENCIES_TOTAL, frequency_step))
    return frequencies_abcisa


def print_spectrum(spectrum):
    plt.interactive(True)
    frequencies = map(lambda spectrum_value: spectrum_value.frequency, spectrum.values)
    intensity = map(lambda spectrum_value:  abs(complex(spectrum_value.real, spectrum_value.img)), spectrum.values)
    plt.plot(frequencies, intensity)
    plt.interactive(True)

def fft_definitive(data):
    ys = numpy.abs(numpy.fft.fft(data)[0:len(data)/2])
#     https://www.youtube.com/watch?v=aQKX3mrDFoY


def fft_harden(data,trimBy=1,logScale=False,divBy=0):
    min_pow_greater_than_data = 262144
    data = numpy.append(data, ([0] * (min_pow_greater_than_data - len(data))))
    scale = (float(RATE)/float(len(data)))
    fft_data = numpy.fft.fft(data)
    fft_data = fft_data * scale*4.11351237396663e-09
    ys = numpy.abs(fft_data) #fft_abs_data =
    #ys = ys / 131072.0
    #left,right=numpy.split(fft_abs_data,2)
    #=numpy.add(left,right[::-1])
    if logScale:
        ys=numpy.multiply(20,numpy.log10(ys))
    xs=numpy.arange(len(data)/2,dtype=float)
    if trimBy:
        i=int((len(data)/2)/trimBy)
        ys=ys[:i]
        xs=xs[:i]*RATE/len(data)
    if divBy:
        ys=ys/float(divBy)
    return xs,ys


def convertir_spectrum(data):
    min_pow_greater_than_data = 262144
    data = numpy.append(data, ([0] * (min_pow_greater_than_data - len(data))))
    scale = (float(RATE) / float(len(data)))
    fft_data = numpy.fft.fft(data)
    fft_data = fft_data * scale * 4.11351237396663e-09
    xs=numpy.arange(len(data)/2,dtype=float)
    i=int((len(data)/2))
    fft_data=fft_data[:i]
    #TODO: it should be in the constructor of the object spectrum
    frequency_step = float(RATE)/len(data)
    xs=xs[:i]*frequency_step
    return xs,fft_data,frequency_step

def convertir_ltas(spectrum_frecuencies, spectrum_complex_values, ancho_banda, my_frequency_step):
    numero_bandas = int(ceil(max_frequency/ancho_banda))
    densidad_potencia_medias = [None]*numero_bandas
    for banda in range(0, numero_bandas):
        frecuencia_inicio_banda = banda*ancho_banda
        densidad_energia_media = obtener_media(spectrum_frecuencies, spectrum_complex_values, frecuencia_inicio_banda, frecuencia_inicio_banda + ancho_banda, my_frequency_step)
        densidad_potencia_media = densidad_energia_media * my_frequency_step
        densidad_potencia_medias[banda] = -300.0 if densidad_potencia_media == 0.0 else numpy.multiply(10,numpy.log10(densidad_potencia_media/4.0e-10))

    bandas = numpy.arange(numero_bandas, dtype=float)*ancho_banda

    return bandas, densidad_potencia_medias

def obtener_media (spectrum_frecuencies, spectrum_complex_values, frequencia_minima, frequencia_maxima, my_frequency_step) :
	(suma, rango) = 	obtener_suma_rango (spectrum_frecuencies, spectrum_complex_values, frequencia_minima, frequencia_maxima, my_frequency_step);
	return suma / rango;

def obtener_suma_rango(spectrum_frecuencies, spectrum_complex_values, frecuencia_minima, frecuencia_maxima, my_frequency_step):

    numero_muestras_hasta_minima = cantidad_muestras_desde_inicio_a_frecuency(frecuencia_minima, my_frequency_step)
    numero_muestras_hasta_maxima = cantidad_muestras_desde_inicio_a_frecuency(frecuencia_maxima, my_frequency_step)
    total_muestras = float(len(spectrum_frecuencies))
    if (numero_muestras_hasta_maxima < 0.5 or numero_muestras_hasta_minima >= total_muestras + 0.5):
        return 0.0, 0.0

    suma = 0.0
    rango = 0.0
    numero_muestras_hasta_minima_redondeado = int(0 if numero_muestras_hasta_minima < 0.5 else round(numero_muestras_hasta_minima))
    numero_muestras_hasta_maxima_redondeado = int(total_muestras if numero_muestras_hasta_maxima >= (total_muestras + 0.5) else round(numero_muestras_hasta_maxima))

    for index  in range(numero_muestras_hasta_minima_redondeado + 1, numero_muestras_hasta_maxima_redondeado):
        value = get_energy_density(index, spectrum_complex_values)
        rango += 1.0
        suma += value

    if numero_muestras_hasta_minima_redondeado == numero_muestras_hasta_maxima_redondeado:
        value = get_energy_density(numero_muestras_hasta_minima_redondeado, spectrum_complex_values)
        fase = numero_muestras_hasta_maxima - numero_muestras_hasta_minima
        rango += fase
        suma += fase * value
    else:
        if numero_muestras_hasta_minima_redondeado >= 1:
            value = get_energy_density(numero_muestras_hasta_minima_redondeado, spectrum_complex_values)
            fase = numero_muestras_hasta_minima_redondeado - numero_muestras_hasta_minima + 0.5
            rango += fase
            suma += fase * value
        if numero_muestras_hasta_maxima_redondeado < total_muestras:
            value = get_energy_density(numero_muestras_hasta_maxima_redondeado, spectrum_complex_values)
            fase = numero_muestras_hasta_maxima - numero_muestras_hasta_maxima_redondeado + 0.5
            rango += fase
            suma += fase * value

    return suma, rango

def cantidad_muestras_desde_inicio_a_frecuency(frequency, my_frequency_step):
	result = (frequency)/my_frequency_step + 1.0
	return result


def get_energy_density(frequency_index, spectrum_complex_values):
    complex = spectrum_complex_values[frequency_index]
    energyDensity = 2.0 * (complex.real*complex.real + complex.imag*complex.imag)
    return energyDensity


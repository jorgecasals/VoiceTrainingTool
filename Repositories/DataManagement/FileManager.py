import os
import wave

import pyaudio

from Playground.Logger import Logger


class FileManager:

    def __init__(self):
        self.RATE = 44100
        self.py_audio = pyaudio.PyAudio()
        self.name = 'FileManager'
        self.reading_size = 1024 * 8

    def get_all_names(self, path_builder):
        elements = os.listdir(path_builder.path)
        return elements

    def get_count(self, path_builder):
        elements = self.get_all_names(path_builder.path)
        elements_count = len(elements)
        return elements_count

    def create(self, content, path_builder):
        with open(path_builder.path, 'a+') as f:
            f.write(content)
            f.close()

    def create_wav(self, sound, path_builder):
        try:
            Logger.info(self, "creating file with audio recorded")

            audio_file = wave.open(path_builder.path, 'w')
            audio_file.setnchannels(1)
            sample_size = self.py_audio.get_sample_size(pyaudio.paInt16)
            audio_file.setsampwidth(sample_size)
            audio_file.setframerate(self.RATE)
            for buffer in sound:
                audio_file.writeframes(buffer)
            audio_file.close()

            Logger.info(self, "saved file")
        except Exception, e:
            Logger.error(self, str(e))

    def get_wav(self, path_builder):
        try:
            audio_file = wave.open(path_builder.path, 'r')
            data = []
            frames = audio_file.readframes(self.reading_size)
            while len(frames) > 0:
                data.append(frames)
                frames = audio_file.readframes(self.reading_size)


            Logger.info(self, "audio readed from file successfully")
            return data

        except Exception, e:
            Logger.error(self, str(e))

    def create_dir(self, name, path_builder):
        if not os.path.exists(path_builder.path + '\\' + name):
            os.makedirs(path_builder.path + '\\' + name)

    def get_content(self, path_builder):
        with open(path_builder.path, 'r') as file:
            data = file.read()
            return data

    def exist(self, path_builder):
        exist = os.path.exists(path_builder.path)
        return exist


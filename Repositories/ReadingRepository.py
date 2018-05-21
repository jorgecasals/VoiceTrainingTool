#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Entities.Reading import Reading
from DataManagement.FileManager import FileManager
from DataManagement.PathBuilders import *

class ReadingRepository:
    def __init__(self):
        self.fileManager = FileManager()

    def get_available_readings(self):
        path_builder = ReadingsDirPathBuilder()
        reading_names = self.fileManager.get_all_names(path_builder)
        readings = []
        for reading_name in reading_names:
            path_builder = ReadingFileInfoPathBuilder(reading_name)
            text = self.fileManager.get_content(path_builder)
            reading = Reading(reading_name, text)
            readings.append(reading)
        return readings

    def get_reading(self, reading_title):
        path_builder = ReadingFileInfoPathBuilder(reading_title)
        text = self.fileManager.get_content(path_builder)
        reading = Reading(reading_title, text)
        return reading
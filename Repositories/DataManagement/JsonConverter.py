import json
from numpy import ndarray
import datetime

class JsonConverter:
    def __init__(self, type_builder):
        self.type_builder = type_builder

    def convert_from_json(self, json_data):
        instance_from_json = self.type_builder()
        properties_dict = eval(json_data)
        instance_from_json.__dict__.update(properties_dict)
        return instance_from_json

    def convert_to_json(self, object):
        object_dictionary = object.__dict__
        json_data = json.dumps(object_dictionary, indent=4, sort_keys=True, default= self.better_str)
        return json_data

    def better_str(self, data):
        if isinstance(data, datetime.datetime):
            return data.__str__()
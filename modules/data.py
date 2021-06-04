"""
Parent class for Youtube data related classes, methods and variables.
"""
import yaml
import os.path
from googleapiclient.discovery import build

class Data:
    def __init__(self):
        dict_variables = self.load_yaml(os.path.dirname(__file__) + "/../variables.yaml")
        for key in dict_variables.keys():
            setattr(self, key, dict_variables[key])
        self.youtube_obj = build(self.youtube_api_name, self.youtube_version, developerKey=self.api_key)
        return

    def load_yaml(self, path_file):
        # Load YAML file
        with open(path_file) as file_yaml:
            return(yaml.load(file_yaml, Loader=yaml.FullLoader))

if(__name__=="__main__"):
    Data()
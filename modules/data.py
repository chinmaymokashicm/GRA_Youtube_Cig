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
    
    def generate_url(self, kind, kind_ID):
        """Generates URL to the video, channel (or other valid entity)

        Args:
            kind (str): Kind of video. Found in search results
            kind_ID (str): ID of the entity. Found in search results
        """
        if("video" in kind):
            url = "https://youtube.com/watch?v={}".format(kind_ID)
        elif("channel" in kind):
            url = "https://youtube.com/channel/{}".format(kind_ID)
        else:
            url = None
        return(url)

if(__name__=="__main__"):
    Data()
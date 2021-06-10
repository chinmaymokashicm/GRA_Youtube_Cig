"""
Parent class for Youtube data related classes, methods and variables.
"""
import yaml
import json
import os.path
from googleapiclient.discovery import build
from datetime import datetime,timezone

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
    
    def generate_filename(self, id, suffix):
        """Generates filename

        Args:
            id (str): Identifier or key word
            suffix (str): Suffix
        """
        now_utc = datetime.now(timezone.utc)
        filename = self.save_file_whitespace_substitute.join(id.split()) + self.save_file_results_separator + str(now_utc) + self.save_file_results_separator + suffix
        return(filename)

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

    def save_json(self, dict_json, filename, path_directory=None):
        """Saves the given dictionary as JSON

        Args:
            dict_json (dict): dictionary to be saved
            filename (str): File name
            path_directory (str, optional): Path of the directory. Defaults to None.
        """
        if(path_directory is None):
            path_directory = self.dir_results
        try:
            with open(os.path.join(path_directory, filename) + ".json", "w") as file_json:
                json.dump(dict_json, file_json)
                return(True)
        except Exception as e:
            print(e)
            return(False)

if(__name__=="__main__"):
    Data()
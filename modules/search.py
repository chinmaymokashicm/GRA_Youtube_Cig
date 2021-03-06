"""
Class for Youtube search related methods and variables.
Inherits from Data Class.
"""
from http.client import responses
from .data import Data

import os.path
from googleapiclient.discovery import build
import pandas as pd
import json
import csv
from datetime import datetime,timezone


class Search(Data):
    def __init__(self):
        super().__init__()

    def search(self, query, max_results=25, url_only=False, save=False, return_table=True, *args, **kwargs):
        """Returns results to searches on Youtube

        Args:
            query (str): Search string.
            max_results (str, optional): Maximum number of results. Defaults to 25
            url_only (bool, optional): If True, will return URLs of the videos only. Defaults to False.
        """
        api_max_results = 50 #The meaximum number of results the API returns

        remaining_results = max_results
        next_page_token = None
        number_of_pages = 1
        list_dict_search_results = []

        if(max_results > api_max_results):
            if(max_results % api_max_results == 0):
                number_of_pages = max_results // api_max_results
            else:
                number_of_pages = max_results // api_max_results + 1

        for _ in range(number_of_pages):
            # print(remaining_results)
            request = self.youtube_obj.search().list(
                part="snippet",
                maxResults=api_max_results if(remaining_results > api_max_results) else remaining_results,
                q=query,
                pageToken=next_page_token,
                *args,
                **kwargs
            )
            response = request.execute()
            list_dict_search_results.append(response)
            next_page_token = response["nextPageToken"]
            remaining_results = remaining_results - api_max_results

        # Convert it to a table if "return_table" is True and return
        if(return_table):
            df = self.convert_search_results_to_table(list_dict_search_results, is_file=False, save=True if save else False, search_query=query)
            return(df)

        # Save the results if "save" is True and return_table is False
        if(save):
            self.save_json(list_dict_search_results, self.generate_filename(id=query, suffix="search"))

        return(list_dict_search_results)

    def convert_search_results_to_table(self, path_json_file, is_file=True, save=False, search_query=None, path_directory=None):
        """Returns search results as pandas table

        Args:
            path_json_file (str): Path to JSON file. If "is_file" is False consider this as a list of dictionary variable
            is_file (bool, optional): Whether "path_json_file" is path to a file or a dictionary variable. Defaults to True.
            save (bool, optional): Save the table as CSV. Defaults to False.
            search_query (str): Valid if "is_file" is False.
            path_directory (str): Path of the directory. Valid if "save" is True. Defaults to None
        """
        if(path_directory is None):
            path_directory = self.dir_results

        if(not is_file):
            list_dict_results = path_json_file
            if(search_query is None):
                search_query = "N.A."
        else:
            with open(path_json_file) as file:
                list_dict_results = json.load(file)
            search_query = "\s".join(os.path.basename(path_json_file).split(self.save_file_results_separator)[0].split(self.save_file_whitespace_substitute))
            # print(search_query)
        list_rows = []
        for dict_results in list_dict_results:
            for dict_item in dict_results["items"]:
                dict_row = {
                    "kind": None,
                    "kind_ID": None,
                    "url": None,
                    "channel_ID": None,
                    "title": None,
                    "channel_title": None,
                    "publish_time": None
                }
                try:
                    for key, value in dict_item["id"].items():
                        if(key == "kind"):
                            dict_row["kind"] = value
                        if("Id" in key):
                            dict_row["kind_ID"] = value
                    if(dict_row["kind"] is not None and dict_row["kind_ID"] is not None):
                        dict_row["url"] = self.generate_url(dict_row["kind"], dict_row["kind_ID"])
                    dict_row["channel_ID"] = dict_item["snippet"]["channelId"]
                    dict_row["title"] = dict_item["snippet"]["title"]
                    dict_row["channel_title"] = dict_item["snippet"]["channelTitle"]
                    dict_row["publish_time"] = dict_item["snippet"]["publishTime"]
                    list_rows.append(dict_row)
                except Exception as e:
                    print(e)
                    # return(False)
        df = pd.DataFrame(list_rows)
        # Save the dataframe as CSV if "save" is True
        if(save):
            path_csv = os.path.join(path_directory, self.generate_filename(id=search_query, suffix="search")) + ".csv"
            df.to_csv(path_csv, index=False, quoting=csv.QUOTE_ALL)
        return(df)

if(__name__=="__main__"):
    Search().search()
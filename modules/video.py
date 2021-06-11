"""
Class for Youtube video related methods and variables.
Inherits from Data Class.
"""
from http.client import responses
from .data import Data

from datetime import datetime,timezone
import json
import os
import pandas as pd
import csv

class Video(Data):
    def __init__(self):
        super().__init__()
    
    def get_video_info(self, video_ID, save=True, all_info=False):
        """Gets JSON showing video information

        Args:
            video_ID (str): video_ID
            save (bool, optional): Whether to save the JSON. Defaults to True.
        """
        request = self.youtube_obj.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ID
        )
        dict_results = request.execute()
        if(not all_info):
            try:
                dict_item = dict_results["items"][0]
                dict_results = {
                    "video_url": self.generate_url(kind="video", kind_ID=video_ID),
                    "video_title": dict_item["snippet"]["title"],
                    "video_description": dict_item["snippet"]["description"],
                    "view_count": dict_item["statistics"]["viewCount"],
                    "like_count": dict_item["statistics"]["likeCount"] if "likeCount" in dict_item["statistics"] else -1,
                    "dislike_count": dict_item["statistics"]["dislikeCount"] if "dislikeCount" in dict_item["statistics"] else -1,
                    "favorite_count": dict_item["statistics"]["favoriteCount"],
                    "comment_count": dict_item["statistics"]["commentCount"] if "commentCount" in dict_item["statistics"] else -1,
                    "channel_url": self.generate_url(kind="channel", kind_ID=dict_item["snippet"]["channelId"]),
                    "publish_time": dict_item["snippet"]["publishedAt"],
                    "video_duration": dict_item["contentDetails"]["duration"]
                }
            except Exception as e:
                print(e)
                print("Could not retrieve specific information for video_ID {}. Returning entire JSON.".format(video_ID))
        if(save):
            self.save_json(dict_json=dict_results, filename=self.generate_filename(id=video_ID, suffix="video_info"))
        return(dict_results)

    def get_comment_threads_to_video(self, video_ID, return_table=False, save=True, *args, **kwargs):
        """Get comments threads to the given video

        Args:
            video_ID (str): Video ID
            save (bool, optional): Whether to save the file. Defaults to True.
        """
        request = self.youtube_obj.commentThreads().list(
            part="snippet,replies",
            videoId=video_ID,
            *args,
            **kwargs
        )
        response = request.execute()
        if(save):
            # self.save_comment_threads(video_ID=video_ID, dict_comments_thread=response)
            self.save_json(dict_json=response, filename=self.generate_filename(id=video_ID, suffix="comments_thread"))

        if(return_table):
            df = self.convert_comment_thread_to_table(path_json_file=response, is_file=False, save=True if save else False, video_ID=video_ID)
            return(df)

        return(response)

    def convert_comment_thread_to_table(self, path_json_file, is_file=True, save=False, video_ID=None, path_directory=None):
        """Converts comment thread JSON to a pandas dataframe

        Args:
            path_json_file (str): Path of the JSON file
            is_file (bool, optional): Whether the "path_json_file" is True. Else, considers the variable as a dictionary. Defaults to True.
            save (bool, optional): Saves the table. Defaults to False.
            video_ID (str): Valid if "is_file" is False.
            path_directory (str): Path of the directory. Valid if "save" is True. Defaults to None.
        """
        if(path_directory is None):
            path_directory = self.dir_results

        if(not is_file):
            dict_results = path_json_file
            if(video_ID is None):
                video_ID = "N.A."
        else:
            with open(path_json_file) as file:
                dict_results = json.load(file)
            video_ID = "\s".join(os.path.basename(path_json_file).split(self.save_file_results_separator)[0].split(self.save_file_whitespace_substitute))
        list_rows = []
        for dict_item in dict_results["items"]:
            dict_row = {
                "video_ID": None,
                "comment_thread_ID": None,
                "comment_ID": None,
                "comment": None,
                "author_channel_ID": None,
                "like_count": None,
                "updated_at": None,
                "publish_time": None
            }
            try:
                dict_row["video_ID"] = dict_item["snippet"]["videoId"]
                dict_row["comment_thread_ID"] = dict_item["id"]
                list_comment_IDs = [dict_item["snippet"]["topLevelComment"]["id"]]
                list_comments = [dict_item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]]
                list_author_channel_IDs = [dict_item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]]
                list_like_count = [dict_item["snippet"]["topLevelComment"]["snippet"]["likeCount"]]
                list_updated_at = [dict_item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]]
                list_published_at = [dict_item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]]
                if("replies" in dict_item):
                    for dict_comment in dict_item["replies"]["comments"]:
                        list_comment_IDs.append(dict_comment["id"])
                        list_comments.append(dict_comment["snippet"]["textOriginal"])
                        list_author_channel_IDs.append(dict_comment["snippet"]["authorChannelId"]["value"])
                        list_like_count.append(dict_comment["snippet"]["likeCount"])
                        list_updated_at.append(dict_comment["snippet"]["updatedAt"])
                        list_published_at.append(dict_comment["snippet"]["publishedAt"])
                for i in range(len(list_comment_IDs)):
                    dict_row = {
                        "video_ID": dict_row["video_ID"],
                        "comment_thread_ID": dict_row["comment_thread_ID"],
                        "comment_ID": list_comment_IDs[i],
                        "comment": list_comments[i],
                        "author_channel_ID": list_author_channel_IDs[i],
                        "like_count": list_like_count[i],
                        "updated_at": list_updated_at[i],
                        "publish_time": list_published_at[i]
                    }
                    list_rows.append(dict_row)
            except Exception as e:
                print(e)
                # return(False)
        df = pd.DataFrame(list_rows)
        # Save the dataframe as CSV if "save" is True
        if(save):
            path_csv = os.path.join(path_directory, self.generate_filename(id=video_ID, suffix="comments_thread")) + ".csv"
            df.to_csv(path_csv, index=False, quoting=csv.QUOTE_ALL)
        return(df)

if(__name__=="__main__"):
    print(Video().get_comment_threads_to_video(video_ID="idke3CW02Sg"))
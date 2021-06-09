from modules.search import Search
from modules.video import Video

import pandas as pd
import yaml
from datetime import datetime
import os

youtube_search_obj = Search()
youtube_video_obj = Video()

# Variables loaded from the variables.yaml file
with open("variables.yaml") as file_yaml:
    dict_variables = yaml.load(file_yaml, Loader=yaml.FullLoader)

list_queries = dict_variables["query_terms"]
number_of_search_results = dict_variables["number_of_search_results"]
number_of_comment_threads = dict_variables["number_of_comment_threads"]


for query in list_queries:
    # Getting the search results
    df_search = youtube_search_obj.search(query=query, max_results=number_of_search_results, type="video", return_table=True)
    # Looping through the videos in the search results
    list_df_video_comments = []
    for video_ID in df_search[df_search["kind"].str.contains("video")]["kind_ID"].to_list():
        try:
            # Getting comment threads to the video
            list_df_video_comments.append(youtube_video_obj.get_comment_threads_to_video(video_ID=video_ID, maxResults=30, return_table=True))
        except Exception as e:
            str_error = "Could not retrieve comments for video_ID: {}".format(video_ID)
            print(str_error)
            print(e)
        else:
            # Getting a combined dataframe
            df_combined = pd.concat(list_df_video_comments, ignore_index=True)
            df_search_and_comments = pd.merge(df_search, df_combined, how="left", left_on="kind_ID", right_on="video_ID", suffixes=["_video", "_comment"])
            df_search_and_comments = df_search_and_comments[
                ["url", "channel_ID", "title", "channel_title", "comment", "author_channel_ID", "like_count", "publish_time_video", "publish_time_comment"]
            ]
            # df_search_and_comments["like_count"] = df_search_and_comments["like_count"].astype(int)
            df_search_and_comments.insert(
                loc=5, 
                column="author_channel", 
                value=df_search_and_comments["author_channel_ID"].apply(
                    lambda video_ID: youtube_search_obj.generate_url(kind="channel", kind_ID=video_ID)
            ))
            df_search_and_comments = df_search_and_comments.drop(["author_channel_ID"], axis=1)

            # Saving the search results in a CSV
            now_date = datetime.now()
            df_search_and_comments.to_csv(
                os.path.join(
                    "generated_tables",
                    "{}{}{}.csv".format(query, dict_variables["save_file_results_separator"], str(now_date))
                    ),
                index=False
            )
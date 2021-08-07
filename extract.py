from modules.search import Search
from modules.video import Video

import pandas as pd
import yaml
from datetime import datetime
import os
from tqdm import tqdm

youtube_search_obj = Search()
youtube_video_obj = Video()

# Variables loaded from the variables.yaml file
with open("variables.yaml") as file_yaml:
    dict_variables = yaml.load(file_yaml, Loader=yaml.FullLoader)

list_queries = dict_variables["query_terms"]
number_of_search_results = dict_variables["number_of_search_results"]
number_of_comment_threads = dict_variables["number_of_comment_threads"]

list_video_IDs_all = []
for query in tqdm(list_queries, desc="Queries..."):
    df_search = youtube_search_obj.search(query=query, max_results=number_of_search_results, type="video", return_table=True, save=False)
    list_video_IDs = df_search[df_search["kind"].str.contains("video")]["kind_ID"].to_list()
    list_video_IDs_all = list_video_IDs_all + [video_ID for video_ID in list_video_IDs]

list_video_IDs_all = list(set(list_video_IDs_all))

list_dict_video_info = []
list_df_comment_threads = []

for video_ID in tqdm(list_video_IDs_all, desc="Videos..."):
    try:
        dict_video_info = youtube_video_obj.get_video_info(video_ID=video_ID, save=False)
        list_dict_video_info.append(dict_video_info)
    except Exception as e:
        print(e)
        print(video_ID)
    try:
        df_comment_thread = youtube_video_obj.get_comment_threads_to_video(video_ID=video_ID, return_table=True, save=False, max_results=number_of_comment_threads)
        list_df_comment_threads.append(df_comment_thread)
    except Exception as e:
        print(e)
        print(video_ID)

df_video_info_all = pd.DataFrame(list_dict_video_info)
df_comment_threads_all = pd.concat(list_df_comment_threads, ignore_index=True)

dir_saved = "generated_tables"
df_video_info_all.to_csv(os.path.join(dir_saved, "video_info") + ".csv", index=False)
df_comment_threads_all.to_csv(os.path.join(dir_saved, "comment_threads") + ".csv", index=False)
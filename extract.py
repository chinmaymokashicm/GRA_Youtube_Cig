from modules.search import Search
from modules.video import Video

import pandas as pd

youtube_search_obj = Search()
df_search = youtube_search_obj.search(query="vaping", max_results=5, type="video", return_table=True)

youtube_video_obj = Video()
df_comments = youtube_video_obj.get_comment_threads_to_video(video_ID="idke3CW02Sg", maxResults=10, return_table=True)


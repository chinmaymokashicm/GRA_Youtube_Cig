from modules.search import Search
from modules.video import Video
from googleapiclient.discovery import build

# youtube_search_obj = Search()
# print(youtube_search_obj.search(query="vaping", max_results=2, type="channel", return_table=True))

youtube_video_obj = Video()
print(youtube_video_obj.get_comment_threads_to_video(video_ID="idke3CW02Sg", maxResults=2))
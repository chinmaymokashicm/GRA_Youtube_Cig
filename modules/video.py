"""
Class for Youtube video related methods and variables.
Inherits from Data Class.
"""
from .data import Data

class Video(Data):
    def __init__(self):
        super().__init__()
    
    def get_comment_threads_to_video(self, video_ID, *args, **kwargs):
        request = self.youtube_obj.commentThreads().list(
            part="snippet,replies",
            videoId=video_ID,
            *args,
            **kwargs
        )
        response = request.execute()
        return(response)
    

if(__name__=="__main__"):
    print(Video().get_comment_threads_to_video(video_ID="idke3CW02Sg"))
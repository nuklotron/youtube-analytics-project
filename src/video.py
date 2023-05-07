import os
from googleapiclient.discovery import build


class Video:
    """Класс для информации по id-видео"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        self.__id_video = id_video
        self.video_info = self.youtube.videos().list(id=self.__id_video, part='snippet,statistics').execute()
        self.title = self.video_info["items"][0]["snippet"]["title"]
        self.link = f'https://youtu.be/{self.__id_video}'
        self.views = self.video_info["items"][0]["statistics"]["viewCount"]
        self.likes = self.video_info["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.title

    @property
    def channel_id(self):
        return self.__id_video


class PLVideo(Video):
    """Класс для информации по id-видео из playlist"""
    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id

import isodate
import json
import os
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    """Класс для информации по id-плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.pl_info = self.youtube.playlists().list(part='contentDetails,snippet', id=self.pl_id).execute()
        self.info = json.dumps(self.pl_info, indent=2, ensure_ascii=False)
        self.title = self.pl_info["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()
        self.video_response_info = json.dumps(self.video_response, indent=2, ensure_ascii=False)

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста (обращение как к свойству)
        """

        total_duration = timedelta(hours=0, minutes=0, seconds=0)

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        video_dict = {}

        for video in self.video_response["items"]:
            like_count = video["statistics"]["likeCount"]
            video_id = video["id"]
            video_dict[int(like_count)] = video_id

        video_dict_ = sorted(video_dict, reverse=True)

        for k, v in video_dict.items():
            if k == video_dict_[0]:
                return f"https://youtu.be/{v}"

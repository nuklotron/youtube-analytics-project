import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.description = self.channel_info["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.channel_info["items"][0]["id"]}'
        self.subs = self.channel_info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel_info["items"][0]["statistics"]["videoCount"]
        self.views = self.channel_info["items"][0]["statistics"]["viewCount"]
        self.__service = self.youtube

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subs) + int(other.subs)

    def __sub__(self, other):
        return int(self.subs) - int(other.subs)

    def __lt__(self, other):
        return int(self.subs) < int(other.subs)

    def __le__(self, other):
        return int(self.subs) <= int(other.subs)

    def __gt__(self, other):
        return int(self.subs) > int(other.subs)

    def __ge__(self, other):
        return int(self.subs) >= int(other.subs)

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        printj = json.dumps(self.channel_info, indent=2, ensure_ascii=False)
        return printj

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, name):
        with open(f"../homework-2/{name}", "w", encoding="utf-8") as f:
            json.dump(self.channel_info, f, sort_keys=True, indent=2, ensure_ascii=False)

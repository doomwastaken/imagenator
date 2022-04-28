import json
import typing

import requests


def encode_message(message: str) -> str:
    return message.replace(r"-", r"\-").replace(r"_", r"\_").replace(r"*", r"\*")


class Bot:
    """VK Teams api wrapper"""

    def __init__(self, token: str) -> None:
        self.token: str = token
        self.base_api_url: str = "https://api.internal.myteam.mail.ru/bot/v1"
        self.send_text_url: str = f"{self.base_api_url}/messages/sendText"

    def send(self, to: str, message: str) -> None:
        """Send message to VK teams chat"""
        params: dict = {
            "token": self.token,
            "chatId": to,
            "text": encode_message(message),
            "parseMode": "MarkdownV2",
        }
        r: requests.Response = requests.get(self.send_text_url, params=params)
        if r.status_code != 200:
            print(f"Request was failed: {r.status_code}")

        resp: typing.Any = r.json()
        if not resp.get("ok", False):
            print(f"Cannot send message: {message} {to}" f"{json.dumps(resp)}")

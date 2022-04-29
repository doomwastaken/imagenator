import json
import logging
import typing

import requests


def encode(message: str) -> str:
    """Encode special characters"""
    return message.replace(r"-", r"\-").replace(r"_", r"\_").replace(r"*", r"\*")


API_URL = "https://api.internal.myteam.mail.ru/bot/v1"


class Bot:
    """VK Teams api wrapper"""

    def __init__(self, token: str) -> None:
        self.token: str = token

    def send(self, to, message):
        """Send message to VK teams chat"""
        params = {
            "token": self.token,
            "chatId": to,
            "text": message,
            "parseMode": "MarkdownV2",
        }
        r: requests.Response = requests.get(
            f"{API_URL}/messages/sendText", params=params
        )
        if r.status_code != 200:
            logging.error(f"failed response code from vk teams api: {r.status_code}")

        resp: typing.Any = r.json()
        if not resp.get("ok", False):
            logging.error(
                f"cannot send message {message} to chat {to}" f"{json.dumps(resp)}"
            )

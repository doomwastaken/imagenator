import json
import logging
import typing

import requests


class Bot:
    """VK Teams api wrapper"""
    api_url = None

    def __init__(self, token: str) -> None:
        self.token: str = token

    def send(self, to, message):
        """Send a message to chat"""
        r: requests.Response = self._send(to, message)
        if r.status_code != 200:
            print(f"failed response code from vk teams api: {r.status_code}")

        resp: typing.Any = r.json()
        if not resp.get("ok", False):
            print(f"cannot send message {message} to chat {to}" f"{json.dumps(resp)}")


class VKTeamsBot(Bot):
    """VK Teams api wrapper"""
    api_url = "https://api.internal.myteam.mail.ru/bot/v1"

    def _send(self, to, message):
        """Send message to VK teams chat"""
        params = {
            "token": self.token,
            "chatId": to,
            "text": message,
            "parseMode": "MarkdownV2",
        }
        return requests.get(f"{self.api_url}/messages/sendText", params=params)


class TelegramBot(Bot):
    """Telegram api wrapper"""
    api_url = "https://api.telegram.org/bot{api_key}/sendMessage"

    def _send(self, to, message):
        """Send message to telegram chat"""
        params = {
            "chat_id": to,
            "text": message,
        }
        return requests.get(self.api_url.format(api_key=self.token), params=params)


def make_bot(bot_type: str, bot_token: str):
    """Make message bot"""
    if bot_type == "VKTeams":
        return VKTeamsBot(bot_token)
    elif bot_type == "telegram":
        return TelegramBot(bot_token)
    else:
        raise ValueError(f"Unknown bot type: {bot_type}")


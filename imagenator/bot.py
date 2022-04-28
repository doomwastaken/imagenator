import json

import requests


class Bot:
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_api_url = "https://api.internal.myteam.mail.ru/bot/v1"
        self.send_text_url = f"{self.base_api_url}/messages/sendText"

    @staticmethod
    def encode_message(message):
        return message.replace(r"-", r"\-").replace(r"_", r"\_").replace(r"*", r"\*")

    def send(self, to, message):
        params = {
            "token": self.token,
            "chatId": to,
            "text": self.encode_message(message),
            "parseMode": "MarkdownV2",
        }
        r = requests.get(self.send_text_url, params=params)
        if r.status_code != 200:
            print(f"Запрос в Myteam завершился с ошибкой {r.status_code}")

        resp = r.json()
        if not resp.get("ok", False):
            print(
                f"Не удалось отправить сообщение {message} {to}" f"{json.dumps(resp)}"
            )

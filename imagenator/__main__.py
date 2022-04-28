from .app import App
from .bot import Bot
from .detector import Detector
from .image import Image
from .settings import BOT_TOKEN


def main():
    app: App = App(bot=Bot(token=BOT_TOKEN), image=Image(), detector=Detector())
    app.scan(
        "registry-gitlab.corp.mail.ru/target-web/target-images/trg-os7-python39:latest"
    )

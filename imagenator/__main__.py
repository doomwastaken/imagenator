import uvicorn

from .api import server
from .app import App
from .bot import Bot
from .detector import Detector
from .image import Image
from .settings import BOT_TOKEN


def main():
    app: App = App(bot=Bot(token=BOT_TOKEN), image=Image(), detector=Detector())
    uvicorn.run(server, host="0.0.0.0", port=8000)

from fastapi import FastAPI, status
from pydantic import BaseModel
from .app import App
from .bot import Bot
from .detector import Detector
from .image import Image
from .settings import BOT_TOKEN


class Handlers:
    def __init__(self, app):
        self.app = app


server = FastAPI()
handle = Handlers(App(bot=Bot(token=BOT_TOKEN), image=Image(), detector=Detector()))


class ImageModel(BaseModel):
    url: str


@server.post("/get_image")
async def get_image(image: ImageModel):
    handle.app.scan(image.url)


@server.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}








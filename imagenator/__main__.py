import asyncio
import logging
import os

import uvicorn
from fastapi import FastAPI, status
from pydantic.dataclasses import dataclass

from .app import App, run
from .bot import Bot
from .detector import Detector
from .image import Image
from .settings import BOT_TOKEN

if os.environ.get("DEBUG", False):
    logging.basicConfig(level=logging.DEBUG)


imagenator: App = App(bot=Bot(token=BOT_TOKEN), image=Image(), detector=Detector())
api: FastAPI = FastAPI()


@api.on_event("startup")
async def startup() -> None:
    """Initialize server tasks for running on event loop"""
    asyncio.create_task(
        run(
            app=imagenator,
            filename=os.environ.get("APP_CONF", "config.json"),
            mins=float(os.environ.get("APP_DURATION", 1)),
        )
    )


@dataclass
class ImageModel:
    url: str


@api.post("/jobs", status_code=status.HTTP_201_CREATED)
async def scan(image: ImageModel):
    """Webhook for scan OCI image"""
    imagenator.send(f"Start scanning image {image.url}")
    try:
        imagenator.scan(image.url)
    except:
        print("error while scanning image request: {image.url}")


@api.get("/ping", status_code=status.HTTP_200_OK)
def healthcheck():
    return


def main():
    uvicorn.run(
        api,
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        port=os.environ.get("APP_PORT", 80),
    )

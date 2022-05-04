import asyncio
import json
import logging

from .bot import Bot
from .cache import Cache
from .detector import Detector, Vulnerability
from .image import Image
from .settings import CHAT_ID


def encode(message: str) -> str:
    """Encode special characters"""
    return message.replace(r"-", r"\-").replace(r"_", r"\_").replace(r"*", r"\*")


class ScanException(BaseException):
    """Raise when error during scanning image"""


class App:
    def __init__(self, bot: Bot, cache: Cache, image: Image, detector: Detector) -> None:
        self.bot = bot
        self.cache = cache
        self.image = image
        self.detector = detector

    def send(self, message: str) -> None:
        """Send message to chat"""
        if not message:
            return
        self.bot.send(CHAT_ID, message)

    def scan(self, image: str) -> None:
        """Scan image for vulnerabilities and publish result"""
        if not image:
            return

        vulnerabilities: list[Vulnerability] = self.detector.check(
            self.cache.cache(image, self.image.decompose),
        )

        if len(vulnerabilities) == 0:
            self.send(f"*Vulnerabilities wasn't detected ✅*```{image}```\n")
            return

        message: str = f"*Image is vulnerable ❌*\n```{image}```\n"
        for vulnerability in vulnerabilities:
            message += (
                f"*{vulnerability.package}:*\n"
                f"- `{vulnerability.version}`\n"
                f"- `{vulnerability.type}`\n"
                f"- [{vulnerability.name}]({encode(vulnerability.link)})\n"
                f"- {encode(vulnerability.description)}\n"
            )
        self.send(message)
        return


async def run(app: App, filename: str, mins: float) -> None:
    """Start shedule job"""
    while True:
        logging.info("Start cron scanning")

        data: dict = dict()
        with open(filename, "r") as f:
            data = json.load(f)

        for image in data.get("images", []):
            try:
                app.scan(image)
            except:
                logging.error(f"error while scanning in cron: {image}")
        await asyncio.sleep(mins * 60)

import json
import asyncio

from .bot import Bot, encode
from .detector import Detector, Vulnerability
from .image import Image
from .settings import CHAT_ID


class ScanException(BaseException):
    """Raise when error during scanning image"""


class App:
    def __init__(self, bot: Bot, image: Image, detector: Detector) -> None:
        self.bot = bot
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
            self.image.decompose(image)
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
        print("Start cron scanning")

        data: dict = dict()
        with open(filename, "r") as f:
            data = json.load(f)

        for image in data.get("images", []):
            try:
                app.scan(image)
            except:
                print(f"error while scanning in cron: {image}")
        await asyncio.sleep(mins * 60)

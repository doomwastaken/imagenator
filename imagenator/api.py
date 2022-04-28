from fastapi import FastAPI, status
from pydantic import BaseModel

server = FastAPI()


class Image(BaseModel):
    url: str


@server.post("/get_image")
async def get_image(image: Image):
    return image


@server.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}
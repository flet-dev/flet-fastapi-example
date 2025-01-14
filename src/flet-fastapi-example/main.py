from contextlib import asynccontextmanager
import asyncio
import flet as ft
import flet_fastapi
from fastapi import FastAPI
import yaml

import gui
import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    asyncio.create_task(idle())
    yield
    await flet_fastapi.app_manager.shutdown()


cfg = yaml.safe_load(open('dockup.yml').read())
path = cfg['path']
name = cfg['name']


app = FastAPI(lifespan=lifespan)

counter = 0


@api.register
@app.get(f'{path}/get-value')
async def get_value():
    return {'message': f'Counter value is currently {counter}'}


@api.register
@app.get(f'{path}/set-value')
async def set_value(value: int):
    global counter
    counter = value
    return {'message': f'Updated counter value to {value}'}


async def idle():
    while True:
        global counter
        counter -= 1
        await asyncio.sleep(1)


async def main(page: ft.Page):
    await gui.init(page, cfg, api.get())

app.mount(f'{path}/', flet_fastapi.app(main))

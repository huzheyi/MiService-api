from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import os
import random
from aiohttp import ClientSession
from pathlib import Path
from miservice import MiAccount, MiNAService, MiIOService, miio_command
from miservice.cli import find_device_id, _get_duration, get_suno_playlist

app = FastAPI()

class PlayRequest(BaseModel):
    url: str

class MessageRequest(BaseModel):
    text: str

class SunoRequest(BaseModel):
    random: bool = False

class MiioCommandRequest(BaseModel):
    command: str
    args: str

async def get_mina_service(session):
    """获取 MiNAService 实例"""
    env = os.environ
    account = MiAccount(
        session,
        env.get("MI_USER"),
        env.get("MI_PASS"),
        os.path.join(str(Path.home()), ".mi.token"),
    )
    return MiNAService(account)

async def get_miio_service(session):
    """获取 MiIOService 实例"""
    env = os.environ
    account = MiAccount(
        session,
        env.get("MI_USER"),
        env.get("MI_PASS"),
        os.path.join(str(Path.home()), ".mi.token"),
    )
    return MiIOService(account)

@app.post("/api/play")
async def play(request: PlayRequest):
    """播放音频"""
    async with ClientSession() as session:
        mina_service = await get_mina_service(session)
        device_id = find_device_id(await mina_service.device_list(), os.environ.get("MI_DID"))
        await mina_service.play_by_url(device_id, request.url)
        return {"status": "playing", "url": request.url}

@app.post("/api/stop")
async def stop():
    """停止播放"""
    async with ClientSession() as session:
        mina_service = await get_mina_service(session)
        device_id = find_device_id(await mina_service.device_list(), os.environ.get("MI_DID"))
        await mina_service.player_stop(device_id)
        return {"status": "stopped"}

@app.post("/api/message")
async def message(request: MessageRequest):
    """文本转语音"""
    async with ClientSession() as session:
        mina_service = await get_mina_service(session)
        device_id = find_device_id(await mina_service.device_list(), os.environ.get("MI_DID"))
        await mina_service.text_to_speech(device_id, request.text)
        return {"status": "message_sent", "text": request.text}

@app.post("/api/suno")
async def suno(request: SunoRequest):
    """播放 Suno 播放列表"""
    async with ClientSession() as session:
        mina_service = await get_mina_service(session)
        device_id = find_device_id(await mina_service.device_list(), os.environ.get("MI_DID"))
        song_dict = await get_suno_playlist(request.random)
        song_urls = list(song_dict.keys())

        if request.random:
            random.shuffle(song_urls)

        for song_url in song_urls:
            title = song_dict[song_url]
            duration = await _get_duration(song_url)
            await mina_service.play_by_url(device_id, song_url.strip())
            await asyncio.sleep(duration)

        await mina_service.player_stop(device_id)
        return {"status": "suno_playlist_finished", "songs_played": len(song_urls)}

@app.post("/api/miio")
async def miio(request: MiioCommandRequest):
    """调用 miio_command"""
    async with ClientSession() as session:
        miio_service = await get_miio_service(session)
        result = await miio_command(
            miio_service,
            os.environ.get("MI_DID"),
            request.command,
            request.args,
        )
        return {"status": "success", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
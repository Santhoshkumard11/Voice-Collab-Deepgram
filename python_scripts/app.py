import logging
import asyncio
import json
from utils import setup_logging, execute_command
import os
from flask import Flask, render_template
from deepgram import Deepgram
from dotenv import load_dotenv
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from typing import Dict, Callable


load_dotenv()

app = Flask("voice_collab", template_folder="./voice-collab-deepgram-templates")

dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))


async def process_audio(ws: web.WebSocketResponse):
    async def get_transcript(data: Dict) -> None:
        if "channel" in data:
            recognized_text = data["channel"]["alternatives"][0]["transcript"]

            if recognized_text:
                logging.info(f"Recognized text - {recognized_text}")

                # this stops the entire server and closes all the websocket connection for a smooth exit
                if recognized_text.find("stop command mode") != -1:
                    logging.info("Closing voice recognizer - user command")
                    await ws.close(3002, "user command - closing connection")
                    await ws.wait_closed()
                    os._exit(0)

                # send the recognized text to execute a command if something matches
                text_to_send = execute_command(recognized_text)

                # if we have any return value send it to the client
                if text_to_send and recognized_text:
                    await ws.send_str(text_to_send)

                if recognized_text:
                    await ws.send_str(recognized_text)

    deepgram_socket = await connect_to_deepgram(get_transcript)

    return deepgram_socket


async def connect_to_deepgram(
    transcript_received_handler: Callable[[Dict], None]
) -> str:
    try:
        socket = await dg_client.transcription.live(
            {"punctuate": True, "interim_results": False}
        )
        socket.registerHandler(
            socket.event.CLOSE, lambda c: print(f"Connection closed with code {c}.")
        )
        socket.registerHandler(
            socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler
        )

        return socket
    except Exception as e:
        raise Exception(f"Could not open socket: {e}")


@app.route("/")
def index():
    return render_template("index.html")


async def socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    deepgram_socket = await process_audio(ws)

    while True:
        data = await ws.receive_bytes()
        deepgram_socket.send(data)


if __name__ == "__main__":
    setup_logging()
    loop = asyncio.get_event_loop()
    aio_app = web.Application()
    wsgi = WSGIHandler(app)
    aio_app.router.add_route("*", "/{path_info: *}", wsgi.handle_request)
    aio_app.router.add_route("GET", "/listen", socket)
    logging.info(f"Server started at {os.getcwd()}")
    web.run_app(aio_app, port=8002)

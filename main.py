from message_bus import MessageBus
import json
from fastapi import FastAPI


async def send_json_message(sender):
    # Convert the JSON object to a string
    message_body = json.dumps({"json": "object"})
    await sender.send(message_body)


app = FastAPI()


@app.get("/")
async def root():
    bus = MessageBus()
    await send_json_message(bus)
    print("Send message is done.")

    return {"message": "Hello World"}

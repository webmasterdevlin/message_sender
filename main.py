import os
import json
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = FastAPI()


# Load connection string and queue name from environment variables
CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_STR")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE_NAME")


# send one queue message
async def send_single_message(sender):
    message = ServiceBusMessage("Single Message")
    await sender.send_messages(message)


# send a list of queue messages
async def send_a_list_of_messages(sender):
    messages = [ServiceBusMessage("Message in list") for _ in range(10)]
    await sender.send_messages(messages)


# send a batch of queue messages
async def send_batch_message(sender):
    batch_message = await sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(ServiceBusMessage("Message inside a ServiceBusMessageBatch"))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    await sender.send_messages(batch_message)


async def send_json_message(sender):
    # Convert the JSON object to a string
    message_body = json.dumps({"json": "object"})
    message = ServiceBusMessage(body=message_body)
    await sender.send_messages(message)


@app.get("/")
async def root():
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

    async with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        async with sender:
            await send_json_message(sender)
            # await send_single_message(sender)
            # await send_a_list_of_messages(sender)
            # await send_batch_message(sender)

    print("Send message is done.")

    return {"message": "Hello World"}

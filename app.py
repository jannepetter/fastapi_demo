from fastapi import FastAPI, HTTPException
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient

app = FastAPI()

SERVICE_BUS_NAMESPACE = "my-service-bus-hommat.servicebus.windows.net"
TOPIC_NAME = "test_topic"
SUBSCRIPTION_NAME = "something"


def fetch_message() -> str | None:
    credential = DefaultAzureCredential()

    with ServiceBusClient(
        fully_qualified_namespace=SERVICE_BUS_NAMESPACE,
        credential=credential,
    ) as client:

        with client.get_subscription_receiver(
            topic_name=TOPIC_NAME,
            subscription_name=SUBSCRIPTION_NAME,
            max_wait_time=10,
        ) as receiver:

            messages = receiver.receive_messages(
                max_message_count=1,
                max_wait_time=10,
            )

            if not messages:
                return None

            message = messages[0]

            body = b"".join(message.body).decode("utf-8")

            receiver.complete_message(message)

            return body



@app.get("/")
async def home():
    return "works"


@app.get("/message")
def get_message():
    message = fetch_message()

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="No messages available",
        )

    return {"message": message}
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    TOKEN: str
    CLONED_PAGE_URL: str
    CHECK_INTERVAL: int
    DATA_FILE: str
    CHANNEL_ID: str | None
    WHATSAPP_API_URL: str
    WHATSAPP_AUTH_TOKEN: str | None
    WHATSAPP_RECIPIENT: str | None
    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_COLLECTION: str


def load_config() -> Config:
    token = os.getenv("TELEGRAM_TOKEN")
    cloned_page_url = os.getenv("CLONED_PAGE_URL")
    mongo_uri = os.getenv("MONGO_URI")

    if not token:
        raise RuntimeError("Missing required config: TELEGRAM_TOKEN")
    if not cloned_page_url:
        raise RuntimeError("Missing required config: CLONED_PAGE_URL")
    if not mongo_uri:
        raise RuntimeError("Missing required config: MONGO_URI")

    return Config(
        TOKEN=token,
        CLONED_PAGE_URL=cloned_page_url,
        CHECK_INTERVAL=int(os.getenv("CHECK_INTERVAL", "10")),
        DATA_FILE=os.getenv("DATA_FILE", "data/notification_data.json"),
        CHANNEL_ID=os.getenv("TELEGRAM_CHANNEL_ID"),
        WHATSAPP_API_URL=os.getenv("WHATSAPP_API_URL", "https://gate.whapi.cloud/messages/text"),
        WHATSAPP_AUTH_TOKEN=os.getenv("WHATSAPP_AUTH_TOKEN"),
        WHATSAPP_RECIPIENT=os.getenv("WHATSAPP_RECIPIENT"),
        MONGO_URI=mongo_uri,
        MONGO_DB_NAME=os.getenv("MONGO_DB_NAME", "apsit_notifier"),
        MONGO_COLLECTION=os.getenv("MONGO_COLLECTION", "notification_state"),
    ) 
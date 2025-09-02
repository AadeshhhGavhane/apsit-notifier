import logging
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class MongoStorage:
    def __init__(self, mongo_uri: str, db_name: str, collection: str):
        self._client = AsyncIOMotorClient(mongo_uri)
        self._db = self._client[db_name]
        self._collection = self._db[collection]
        self._doc_id = "state"

    async def load_state(self) -> Dict[str, Any]:
        try:
            doc = await self._collection.find_one({"_id": self._doc_id})
            if not doc:
                return {}
            data = doc.get("data", {})
            if isinstance(data, dict):
                return data
            return {}
        except Exception as e:
            logger.error(f"Mongo load_state error: {str(e)}")
            return {}

    async def save_state(self, data: Dict[str, Any]) -> None:
        try:
            await self._collection.update_one(
                {"_id": self._doc_id},
                {"$set": {"data": data}},
                upsert=True,
            )
        except Exception as e:
            logger.error(f"Mongo save_state error: {str(e)}")

    async def close(self) -> None:
        self._client.close() 
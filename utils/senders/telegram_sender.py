import asyncio
import logging
from typing import Callable

from telegram.error import TelegramError, RetryAfter, NetworkError

logger = logging.getLogger(__name__)


class TelegramSender:
    def __init__(self, bot, channel_id: str):
        self._bot = bot
        self._channel_id = channel_id

    async def _send_with_backoff(self, send_coro_factory: Callable[[], asyncio.Future], max_retries: int = 5):
        delay = 1.0
        for _ in range(max_retries):
            try:
                return await send_coro_factory()
            except RetryAfter as e:
                sleep_for = max(float(getattr(e, "retry_after", 1)), delay)
                logger.error(f"Rate limited. Retry in {int(sleep_for)}s")
                await asyncio.sleep(sleep_for)
                delay = min(delay * 2, 30)
            except NetworkError as e:
                logger.error(f"Network error: {str(e)}. Retrying in {int(delay)}s")
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
            except TelegramError as e:
                logger.error(f"Telegram error: {str(e)}")
                break
        logger.error("Giving up after retries due to rate limits or network errors")

    async def send_items(self, messages: list[str], spacing_seconds: float = 1.2):
        for message in messages:
            async def _send():
                return await self._bot.send_message(
                    chat_id=self._channel_id,
                    text=message,
                    parse_mode=None,
                    disable_web_page_preview=False,
                )
            await self._send_with_backoff(_send)
            await asyncio.sleep(spacing_seconds) 
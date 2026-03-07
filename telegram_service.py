from telegram import Bot

import bluesky_service
import config as cfg
import json

from datetime import datetime, timezone
from typing import Any
import logging
logger = logging.getLogger(__name__)


TG_TOKEN: str = cfg.config.telegram_token
TG_CHANNEL: str = cfg.config.telegram_channel_id
TG_FOOTER_TXT: str = cfg.config.telegram_footer_txt
tg_bot = Bot(token=TG_TOKEN)
tg_log_file: str = cfg.config.tg_log_file


class TelegramLogger(bluesky_service.PostLogger):
    """Logger for storing Telegram message records in JSON format."""

    def __init__(self, log_file: str = cfg.config.tg_log_file) -> None:
        """Initialise Telegram logger.

        Args:
            log_file: Path to the JSON log file
        """
        super().__init__(log_file)

    def log_post(self, response: Any) -> None:
        """Log a successfully sent Telegram message to file.

        Args:
            response: Response object from Telegram API
        """
        try:
            log_entry = {
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "telegram_message": str(response),
                "message_id": str(response.message_id),
                "chat_id": str(response.chat.id),
            }

            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            logs.append(log_entry)

            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)

            logger.info(f"Telegram message logged to {self.log_file}")
        except Exception as e:
            logger.error(f"Failed to log Telegram message: {e}")

telegram_logger = TelegramLogger()

async def send_to_telegram(message: str) -> None:
    response = await tg_bot.send_message(
        chat_id=TG_CHANNEL,
        text=f"{message}\n\n{TG_FOOTER_TXT}",
        parse_mode="HTML"
    )
    logger.info(f"Response type: {type(response)}")
    logger.info(f"Response: {response}")
    telegram_logger.log_post(response)

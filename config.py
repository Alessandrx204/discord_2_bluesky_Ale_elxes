"""Configuration module for Discord-Bluesky bot."""

import os
from typing import Optional

from dotenv import load_dotenv
load_dotenv()


class Config:
    """Configuration class for managing bot settings."""

    def __init__(self) -> None:
        """Initialize configuration from environment variables."""
        self.discord_token: str = self._get_env("DISCORD_TOKEN")
        self.bluesky_username: str = self._get_env("BLUESKY_USERNAME")
        self.bluesky_password: str = self._get_env("BLUESKY_PASSWORD")
        self.discord_channel_id: int = self._get_env_int("DISCORD_CHANNEL_ID", 0)
        self.max_post_length: int = self._get_env_int("MAX_POST_LENGTH", 300)
        self.bs_log_file: str = self._get_env("BS_LOG_FILE", "Bluesky_log.json")
        self.tg_log_file: str = self._get_env("TG_LOG_FILE", "Telegram_log.json")
        self.log_level: str = self._get_env("LOG_LEVEL", "INFO")
        self.bluesky_footer_txt: str = self._get_env("BS_FOOTER_TXT")
        self.telegram_token: str = self._get_env("TELEGRAM_TOKEN")
        self.telegram_username: str = self._get_env("TELEGRAM_USERNAME")
        self.telegram_channel_id: str = self._get_env("TG_CHANNEL_ID")
        self.telegram_footer_txt: str = self._get_env("TG_FOOTER_TXT")


    @staticmethod
    def _get_env(key: str, default: Optional[str] = None) -> str:
        """Get environment variable with optional default value.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
            
        Raises:
            ValueError: If required variable is not found and no default provided
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    @staticmethod
    def _get_env_int(key: str, default: int = 0) -> int:
        """Get environment variable as integer.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value as int or default
        """
        try:
            return int(os.getenv(key, default))
        except ValueError:
            return default


# Global config instance
config = Config()

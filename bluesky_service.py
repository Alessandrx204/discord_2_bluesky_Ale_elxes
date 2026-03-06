"""Bluesky service module for posting content."""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict
from dotenv import load_dotenv
load_dotenv()
from atproto import Client
from config import config
logger = logging.getLogger(__name__)


class BlueskyService:
    """Service for interacting with Bluesky API."""

    # Footer text is loaded from the config.py file
    FOOTER_TEXT: str = config.bluesky_footer_txt

    def __init__(self, username: str, password: str) -> None:
        """Initialize Bluesky service and authenticate.
        
        Args:
            username: Bluesky username
            password: Bluesky password
            
        Raises:
            RuntimeError: If authentication fails
        """
        self.client = Client()
        try:
            self.client.login(username, password)
            logger.info(f"Successfully authenticated with Bluesky as {username}")
        except Exception as e:
            logger.error(f"Failed to authenticate with Bluesky: {e}")
            raise RuntimeError(f"Bluesky authentication failed: {e}") from e

    def post(self, content: str) -> Dict[str, Any]:
        """Post a message to Bluesky.
        
        Args:
            content: The text content to post
            
        Returns:
            Response object from Bluesky API
            
        Raises:
            RuntimeError: If posting fails
        """
        try:
            formatted_content = f"{content}\n\n{self.FOOTER_TEXT}"
            response = self.client.send_post(formatted_content)
            logger.info(f"Posted to Bluesky - URI: {response.uri}")
            return response
        except Exception as e:
            logger.error(f"Failed to post to Bluesky: {e}")
            raise RuntimeError(f"Failed to post to Bluesky: {e}") from e

    def prepare_content(self, raw_text: str) -> str:
        """Prepare and clean content before posting.
        
        Args:
            raw_text: Raw text from user input
            
        Returns:
            Cleaned and prepared text
        """
        return raw_text.strip()


class PostLogger:
    """Logger for storing post records in JSON format."""

    def __init__(self, log_file: str = "posts_log.json") -> None:
        """Initialize post logger.
        
        Args:
            log_file: Path to the JSON log file
        """
        self.log_file = log_file

    def log_post(self, response: Any) -> None:
        """Log a successfully posted message to file.
        
        Args:
            response: Response object from Bluesky API
        """
        try:
            log_entry = {
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "bluesky_post": str(response),
                "uri": str(response.uri),
                "cid": str(response.cid),
            }

            # Read existing logs
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            # Append new entry
            logs.append(log_entry)

            # Write back
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Post logged to {self.log_file}")
        except Exception as e:
            logger.error(f"Failed to log post: {e}")

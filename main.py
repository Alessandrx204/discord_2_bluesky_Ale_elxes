"""Main entry point for Discord-Bluesky bot."""

import sys

from config import config
from logger import setup_logger
from bluesky_service import BlueskyService, PostLogger
from discord_bot import DiscordBot


# Setup logging
logger = setup_logger(
    "discord_bluesky_bot",
    log_level=config.log_level,
)


def main() -> None:
    """Main entry point for the application."""
    try:
        logger.info("Initializing Discord-Bluesky Bot...")
        
        # Initialize services
        bluesky_service = BlueskyService(
            username=config.bluesky_username,
            password=config.bluesky_password
        )

        post_logger = PostLogger(log_file=config.bs_log_file)
        
        # Initialize and run bot
        discord_bot = DiscordBot(bluesky_service, post_logger)
        discord_bot.run()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

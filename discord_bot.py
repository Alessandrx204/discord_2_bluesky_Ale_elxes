"""Discord bot module."""

import logging
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from bluesky_service import BlueskyService, PostLogger
from config import config

logger = logging.getLogger(__name__)


class DiscordBot:
    """Main Discord bot class."""

    MAX_EMPTY_CHECKS = 3

    def __init__(self, bluesky_service: BlueskyService, post_logger: PostLogger) -> None:
        """Initialize the Discord bot.
        
        Args:
            bluesky_service: BlueskyService instance for posting
            post_logger: PostLogger instance for logging posts
        """
        self.bluesky = bluesky_service
        self.logger = post_logger
        
        # Setup intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self._setup_events()
        self._setup_commands()

    def _setup_events(self) -> None:
        """Register bot event handlers."""
        @self.bot.event
        async def on_ready() -> None:
            """Called when the bot is ready."""
            logger.info(f"Bot logged in as {self.bot.user}")
            try:
                synced = await self.bot.tree.sync()
                logger.info(f"Synchronized {len(synced)} slash commands")
            except Exception as e:
                logger.error(f"Failed to sync commands: {e}")

    def _setup_commands(self) -> None:
        """Register slash commands."""
        @self.bot.tree.command(
            name="post",
            description="Post a message to Bluesky",
        )
        @app_commands.describe(text="The text to post on Bluesky")
        async def slash_post(interaction: discord.Interaction, text: str) -> None:
            """Slash command to post to Bluesky.
            
            Args:
                interaction: Discord interaction object
                text: The text to post
            """
            # Validate input
            validation_error = self._validate_post_content(text)
            if validation_error:
                await interaction.response.send_message(
                    validation_error,
                    ephemeral=True,
                )
                return

            # Defer response (API call might take time)
            await interaction.response.defer()

            try:
                # Process content
                processed_text = self.bluesky.prepare_content(text)
                
                # Post to Bluesky
                response = self.bluesky.post(processed_text)
                
                # Log the post
                self.logger.log_post(response)
                
                # Send success feedback
                await interaction.followup.send(
                    f"✅ Successfully posted to Bluesky!\n\n**Posted text:**\n{processed_text}"
                )
                logger.info(f"Post command executed successfully by {interaction.user}")
            except Exception as e:
                logger.error(f"Failed to post: {e}")
                await interaction.followup.send(
                    f"❌ Failed to post to Bluesky: {str(e)}",
                )

    @staticmethod
    def _validate_post_content(text: str) -> Optional[str]:
        """Validate post content before posting.
        
        Args:
            text: Text to validate
            
        Returns:
            Error message if validation fails, None if valid
        """
        if not text or len(text.strip()) == 0:
            return "❌ The text cannot be empty!"
        
        if len(text) > config.max_post_length:
            return f"❌ Text is too long (max {config.max_post_length} characters)!"
        
        return None

    def run(self) -> None:
        """Start the bot."""
        logger.info("Starting Discord bot...")
        self.bot.run(config.discord_token)

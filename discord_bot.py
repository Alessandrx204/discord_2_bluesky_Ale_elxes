"""Discord bot module."""

import logging
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from bluesky_service import BlueskyService, PostLogger
from config import config
from telegram_service import send_to_telegram

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
# commands start here at 53
    def _setup_commands(self) -> None:
        """Register slash commands."""

        # ── internal helpers ──────────────────────────────────────────────────

        async def _do_post(
                self,
                interaction: discord.Interaction,
                text: str,
                *, #free for hypothetical other platforms e.g. mastodon, reddit,  twitter(not X)...
                post_to_bluesky: bool = False,
                post_to_telegram: bool = False,
        ) -> None:
            """Core logic shared by all post commands."""
            validation_error = self._validate_post_content(text)
            if validation_error:
                await interaction.response.send_message(validation_error, ephemeral=True)
                return

            await interaction.response.defer()
            results: list[str] = []

            try:
                if post_to_bluesky:
                    processed_text = self.bluesky.prepare_content(text)
                    response = self.bluesky.post(processed_text)
                    self.logger.log_post(response)
                    results.append(f"✅ Bluesky\n**Posted text:**\n{processed_text}")

                if post_to_telegram:
                    await send_to_telegram(text)
                    results.append(f"✅ Telegram\n**Posted text:**\n{text}")

                await interaction.followup.send("\n\n".join(results))
                logger.info("Post executed successfully by %s", interaction.user)

            except Exception as e:
                logger.exception("Failed to post")
                await interaction.followup.send(f"❌ Failed to post: {e}")

        # ── slash commands ────────────────────────────────────────────────────

        @self.bot.tree.command(name="bs_post", description="Post to Bluesky")
        @app_commands.describe(text="The text to post on Bluesky")
        async def slash_bs_post(interaction: discord.Interaction, text: str) -> None:
            await _do_post(self, interaction, text, post_to_bluesky=True)

        @self.bot.tree.command(name="tg_post", description="Post to Telegram")
        @app_commands.describe(text="The text to post on Telegram")
        async def slash_tg_post(interaction: discord.Interaction, text: str) -> None:
            await _do_post(self, interaction, text, post_to_telegram=True)

        @self.bot.tree.command(name="post_all", description="Post to Bluesky AND Telegram")
        @app_commands.describe(text="The text to post everywhere")
        async def slash_post_all(interaction: discord.Interaction, text: str) -> None:
            await _do_post(self, interaction, text, post_to_bluesky=True, post_to_telegram=True)

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

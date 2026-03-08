# Discord-Bluesky Bot

A modular Discord bot that posts messages to Bluesky and Telegram using slash commands.

## Features

- **Slash Commands**: Easy-to-use `/bs_post` command in Discord for Bluesky
- **Slash Commands**: Easy-to-use `/tg_post` command in Discord for Telegram
- **Slash Commands**: Easy-to-use `/post_all` command in Discord for Bluesky AND Telegram 
- **Bluesky Integration**: Automatically posts messages to Bluesky
- **Logging**: Comprehensive logging with file persistence
- **Input Validation**: Validates message length and content
- **Error Handling**: Robust error handling with user feedback
- **Environment Configuration**: Secure configuration via environment variables

## Project Structure

```
.
├── config.py            # Configuration management
├── logger.py            # Logging setup
├── bluesky_service.py   # Bluesky API service via Atproto
├── telegram_service.py   # Telegram bot API service via Python-telegram-bot lib
├── discord_bot.py       # Discord bot implementation
├── main.py              # Application entry point
├── shell.nix            # NixOS development environment
├── .env.example         # Example environment configuration
└── README.md            # This file
```

## Setup

### Prerequisites

- Python 3.11+ (3.12 is reccomended)
- Discord Bot Token
- Bluesky Account (with App Password)

### Installation

#### 1. Clone/Setup the Project

```
git clone https://github.com/Alessandrx204/Discord-BlueskyBot_Ale_elxes
```

```bash
cd Discord-BlueskyBot_Ale_elxes
```

#### 2. Create Environment File

```bash
cp .env .env
```

Edit `.env` with your credentials:
```env
DISCORD_TOKEN=your_token_here
DISCORD_CHANNEL_ID=your_channel_id
BLUESKY_USERNAME=your_handle.bsky.social
BLUESKY_PASSWORD=your_app_password
TELEGRAM_TOKEN=your_token_here
TG_CHANNEL_ID=your_channel_id
TG_USERNAME=your telegram bot handle(Optional)
BS_FOOTER_TXT=a footer text to apply to every post you make on bluesky social(can be a slogan a disclaime, and adv or empy string)
TG_FOOTER_TXT= Same as BS_FOOTER_TXT but for Telegram posts
```
#### 2a. Create a Python Virtual Environment (venv)

It is recommended to use a virtual environment to isolate dependencies:

```bash
python -m venv venv        # Create the venv
# Activate it:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
#### 3a. On NixOS

```bash
nix-shell --run "python main.py"
```

Or enter the dev environment:
```bash
nix-shell
python main.py
```

#### 3b. On Other Systems

```bash
pip install -r requirements.txt
python main.py
```

## Usage

### Discord Command

In Discord, use the `/bs_post` command:

```
/bs_post Hello, this is my first Bluesky post!
```
` /tg_post` is for telegram and `/post_all` for both.
### Features

- **Max Length**: 300 characters (configurable via `MAX_POST_LENGTH`)
- **Footer**: Automatically adds "*This is an automated account...*"
- **Logging**: All posts are logged to `posts_log.json`
- **Feedback**: Get instant confirmation when posts are sent

## Configuration

Edit `.env` to customize:

```env
# Maximum post length (default: 300)
MAX_POST_LENGTH=300

# Log file location (default: Bluesky_log.json/Telegram_log.json)
BS_LOG_FILE=Bluesky_log.json
TG_LOG_FILE=Telegram_log.json

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
LOG_LEVEL=INFO
```

## Development

### File Descriptions

- **config.py**: Centralized configuration management with environment variables
- **logger.py**: Reusable logger setup with console and file output
- **bluesky_service.py**: Encapsulated Bluesky API interactions
- **discord_bot.py**: Discord bot with slash commands
- **main.py**: Application entry point with error handling
- **telegram_service.py**: Encapsulated Telegram bot interactions

## Troubleshooting

### "Missing required environment variable"
Make sure all required variables are set in `.env`:
- `DISCORD_TOKEN`
- `BLUESKY_USERNAME`
- `BLUESKY_PASSWORD`
- `TELEGRAM_TOKEN`(optional)

### "Failed to authenticate with Bluesky"
Check your Bluesky credentials. Use an **App Password**, not your main password.

### "Synchronized 0 slash commands"
This can happen on first run. Wait a moment and try the command again in Discord.

## Security Notes

- **Never** commit `.env` files with real credentials
- Use environment variables or `.env` files for secrets
- Consider rotating your Bluesky App Password regularly

## License

MIT

## CREDITS

[ELXES04](https://github.com/Elxes04) a great friend and IT teacher, helped take the project quality from the terrible state I left it in to a much higher level.

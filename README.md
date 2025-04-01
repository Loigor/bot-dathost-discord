# Dathost Discord Bot

A Discord bot for managing CS2 game servers on Dathost. The bot allows users to control and monitor game servers directly through Discord commands.

## Project Structure

```
.
├── src/
│   ├── bot.py
│   └── dathost_api.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Features

- **Server Management**
  - Start, stop and restart servers
  - View server status and player counts
  - Get server connection information
  - List all available servers

- **Channel Restrictions**
  - Commands can be restricted to specific Discord channels
  - Clear error messages showing correct channels

- **Easy Connection**
  - Direct `connect` commands for joining servers
  - Server status monitoring
  - Player count tracking

## Commands

- `!servers` - List all available servers
- `!status` - Show currently running servers
- `!start <server name>` - Start a specific server
- `!stop <server name>` - Stop a specific server
- `!restart <server name>` - Restart a specific server
- `!prac` - Quick access to practice server info
- `!ping` - Check bot latency

## Setup

1. Clone the repository
2. Create a `.env` file with required credentials
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python src/bot.py
   ```

## Docker Setup

1. Build and start with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. View logs:
   ```bash
   docker-compose logs -f
   ```

3. Stop the bot:
   ```bash
   docker-compose down
   ```

## Environment Variables

Create a `.env` file in the project root with the following content:

```env
# Discord Bot Token (from Discord Developer Portal)
DISCORD_TOKEN=your_discord_bot_token_here

# Dathost API Credentials
DATHOST_EMAIL=your_dathost_email
DATHOST_PASSWORD=your_dathost_password

# Allowed Discord Channel IDs (comma-separated, no spaces)
ALLOWED_CHANNELS=123456789,987654321

# Practice Server Name (optional, defaults to 'prac')
PRAC_SERVER_NAME=your_practice_server_name
```

## Requirements

- Python 3.11+
- discord.py
- python-dotenv
- aiohttp

Or using Docker:
- Docker
- Docker Compose

## Development

1. Enable Discord Developer Mode to get channel IDs:
   - Open Discord Settings
   - Go to App Settings > Advanced
   - Enable Developer Mode
   - Right-click on a channel and select "Copy ID"

2. Test in a development Discord server first
3. Make sure the bot has necessary permissions in your Discord server

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Regularly rotate your Discord bot token and Dathost credentials
- Restrict bot commands to specific channels for better control
- Use a `.gitignore` file to prevent committing sensitive files

## License

MIT License

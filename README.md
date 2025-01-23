## VALARIFY DISCORD BOT

### Description

Valarify is a Discord bot designed to play music in your server. It is built using Python and leverages the discord.py library to interact with the Discord API.

### Features

- Play music from YouTube
- Queue system for managing songs

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/thefznkhan/ValarifyBot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ValarifyBot
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `.env` file in the project directory and add your Discord bot token:
    ```
    BOT_TOKEN=your_discord_bot_token
    ```

### Usage

1. Run the bot:
    ```bash
    python bot.py
    ```
2. Invite the bot to your Discord server using the OAuth2 URL generated from the Discord Developer Portal.

### Commands

- `!join`: Bot join your voice channel
- `!leave`: Bot leave you voice channel
- `!play <url>`: Play a song from a YouTube URL and add new song to the queue
- `!play_local <song_name>`: Play a song from local files
- `!test_audio`: Play testing audio
- `!stop`: Stop the song

### Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

### License

This project is licensed under the MIT License.
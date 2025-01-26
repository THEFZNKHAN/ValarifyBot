# Valarify Music Bot

## 🎵 Overview
Valarify Music Bot is a feature-rich Discord music bot that allows users to play, download, and manage music directly in their Discord voice channels. With a wide range of commands, users can easily interact with music from YouTube and local sources.

## ✨ Features
- Download audio from YouTube
- Play music from YouTube URLs
- Play local music files
- Advanced queue management
- Multiple playback controls

## 🛠 Prerequisites
Before setting up the bot, ensure you have the following installed:

### Software Requirements
- Python 3.8+
- FFmpeg
- pip (Python package manager)

### Required Python Packages
- discord.py[voice]
- python-dotenv
- yt-dlp
- asyncio
- python-dotenv

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/thefznkhan/ValarifyBot.git
cd ValarifyBot
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. FFmpeg Installation
- **Windows**: Download from [FFmpeg Official Site](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### 5. Discord Bot Setup
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" section and create a bot
4. Copy the bot token

### 6. Configuration
Create a `.env` file in the project root:
```
BOT_TOKEN=your_discord_bot_token_here
```

## 🎮 Commands

### Music Playback
- `!join`: Make the bot join your voice channel
- `!leave`: Make the bot leave the voice channel
- `!play <YouTube URL>`: Play a song from YouTube
- `!download_audio <YouTube URL>`: Download and queue a song
- `!play_local <filename>`: Play a local music file

### Queue Management
- `!queue` or `!q`: Show current music queue
- `!next` or `!skip`: Skip to the next song
- `!previous`: Go back to the previous song
- `!clear`: Stop music and clear queue
- `!pause` or `!stop`: Pause current song
- `!resume`: Resume paused song


## 📁 Project Structure
```
ValarifyBot/
│
├── bot.py           # Main bot configuration
├── .env             # Environment variables
├── requirements.txt # Python dependencies
│
├── cogs/
│   └── music.py     # Music-related commands
│
├── utils/
│   └── queue.py     # Music queue management
│
└── music/           # Local music storage
```

## 🔧 Troubleshooting
- Ensure bot has proper permissions in Discord
- Check that FFmpeg is correctly installed
- Verify all dependencies are installed
- Check Discord bot token is correct

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact
Faizan Khan - [fkhan20040@gmail.com](mailto:fkhan20040@gmail.com)

Project Link: [https://github.com/thefznkhan/ValarifyBot](https://github.com/thefznkhan/ValarifyBot)
# Discord Music Bot

This is a Discord music bot that can play, pause, resume, skip, shuffle, and stop songs in a voice channel. It uses `discord.py`, `ffmpeg`, `yt-dlp`, and `pytube` for handling music playback.

## Prerequisites

- Python 3.8 or higher
- `ffmpeg` installed and added to your system's PATH
- A Discord bot token

## Setup

### 1. Install Python

Download and install Python from the official [website](https://www.python.org/downloads/).

Make sure to add Python to your system's PATH during the installation.

### 2. Install `ffmpeg`

Download `ffmpeg` from the official [website](https://ffmpeg.org/download.html).

After downloading, extract the zip file to a folder, e.g., `C:\ffmpeg`.

Add the `bin` folder to your system's PATH:
1. Open the Start Search, type in "env", and select "Edit the system environment variables".
2. In the System Properties window, click on the "Environment Variables" button.
3. In the Environment Variables window, find the "Path" variable in the "System variables" section, and click "Edit".
4. Click "New" and add the path to the `bin` folder, e.g., `C:\ffmpeg\bin`.
5. Click "OK" to close all windows.

### 3. Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/yourusername/discord-music-bot.git
cd discord-music-bot
```
### 4. Create a .env File
Create a .env file in the root directory of the project and add your Discord bot token:

### 5. Install Dependencies

Install the required dependencies using pip:
```sh
pip install -r requirements.txt
```

### 6. Run the Bot
Run the bot using the following command:

Setting Up a Discord Bot:
- Go to the Discord Developer Portal.
- Click on "New Application" and give it a name.
- Go to the "Bot" tab and click "Add Bot".
- Copy the bot token and add it to your .env file.
- Go to the "OAuth2" tab, select "bot" under "SCOPES", and select the necessary permissions under "BOT PERMISSIONS".
- Copy the generated URL and use it to invite the bot to your server.

Commands:

-play <song>: Play a song or add it to the queue.

-pause: Pause the current song.

-resume: Resume the paused song.

-skip: Skip the current song.

-stop: Stop the current song.

-help: Show the help message.

-queue: Show how many songs are in the queue

-shuffle: Shuffle the queue

**Important Note**

Please be aware that using this bot to play music from YouTube may violate YouTube's terms of service. Discord has enforced stricter policies regarding bots that play music from YouTube, and popular music bots have been shut down as a result. Use this bot responsibly and consider using other sources for music or exploring alternatives that have proper licensing agreements.

This bot was created as a learning project for python and discord bots. While I don't expect anyone to actually use this, I have to mention that I don't support using it for playing youtube videos and this README documents the process I went through as a reference for future projects.

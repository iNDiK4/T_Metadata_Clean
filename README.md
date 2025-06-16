# Telegram Metadata Cleaner Bot

A Telegram bot that removes metadata from JPEG images and adds a custom comment.

## Features
- Removes all EXIF metadata from uploaded JPEG files
- Adds custom comment to processed images
- Shows animated loading indicator during processing
- Handles errors gracefully

## Prerequisites
- Python 3.8+
- `aiogram` library
- `exiftool` installed on system
- Telegram Bot Token

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/telegram-metadata-cleaner.git
```
2. Install dependencies:
```bash
pip install aiogram
```
3. Install `exiftool`:
   - Ubuntu: `sudo apt-get install libimage-exiftool-perl`
   - macOS: `brew install exiftool`

## Usage
1. Set your bot token in the `telegram_bot.py` file:
```python
TOKEN = 'YOUR_BOT_TOKEN'
```
2. Run the bot:
```bash
python telegram_bot.py
```
3. Start the bot in Telegram with `/start` and upload a JPEG file.

## How It Works
- User sends a JPEG file to the bot
- Bot downloads the file and removes all EXIF metadata
- Adds a custom comment to the image
- Sends the processed file back to the user
- Deletes temporary files

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
[MIT](LICENSE)

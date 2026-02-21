# SQLMap Telegram Bot

A Telegram bot interface for SQLMap with interactive features.

## Features

- Interactive option selection with paginated buttons
- Real-time scan output streaming
- Interactive database dump (DB → Table → Columns)
- Session management for multiple users
- Automatic output file attachment

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your Telegram bot token to `.env`:
```
TELEGRAM_TOKEN=your_actual_token
```

4. Run the bot:
```bash
python telegram_bot.py
```

## Commands

- `/start` - Show available commands
- `/sqlmap <URL>` - Start scan with interactive options
- `/dump` - Interactive database dump
- `/continue` - Resume scan with more options

## Usage

1. Start a scan: `/sqlmap http://target.com?id=1`
2. Select options using the interactive buttons
3. Click "Done" to execute
4. Use `/dump` for step-by-step database extraction

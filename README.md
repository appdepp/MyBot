# MyWeatherBot

Telegram bot that returns current weather by user geolocation or city name.

## Features

- Weather by Telegram location
- Weather by city name
- OpenWeather API integration
- Environment-based secret configuration

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` or export variables:

```bash
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export OPENWEATHER_API_KEY="your_openweather_api_key"
```

Run:

```bash
python telegram_bot.py
```

## Security

Do not commit real API keys or bot tokens. Use environment variables or a local `.env` file ignored by Git.

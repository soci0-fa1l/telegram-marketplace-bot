# Telegram Marketplace Bot

This project contains a small web interface built with React and a simple
Telegram bot implemented in `api/bot.py`.

## Installation

### Node dependencies

```bash
npm install
```

### Python dependencies

`api/bot.py` relies only on Python's standard library (`json`, `os`,
`urllib` and `http.server`).  No additional packages are required.  If you
extend the bot to use third-party libraries, list them in
`requirements.txt` and install with:

```bash
pip install -r requirements.txt
```

## Running locally

The React app can be started with:

```bash
npm start
```

The bot handler is designed for serverless environments that pass incoming
Telegram webhook requests to `api/bot.py`.

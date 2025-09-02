# 🔔 APSIT Notifier

Automated notifier that monitors a configured webpage for new notices and broadcasts them to a Telegram channel and WhatsApp via Whapi Cloud. Built with async I/O, MongoDB state storage, and container-first tooling.

## ✨ Features
- 🕒 Periodic fetch from `CLONED_PAGE_URL`
- 🔎 Robust HTML parsing (BeautifulSoup) for known sections
- 🔁 Sends new items only (diffs with MongoDB)
- 📢 Telegram channel broadcasting with rate-limit backoff
- 📲 WhatsApp notifications via Whapi Cloud (optional)
- 🧠 Async and resilient (aiohttp, retries, graceful shutdown)
- 📦 Docker + Compose + uv for fast, reproducible builds

## 📁 Project structure
```
apsit-notifier/
├─ main.py
├─ utils/
│  ├─ config.py
│  ├─ storage.py
│  └─ notification_bot.py
├─ pyproject.toml
├─ uv.lock
├─ Dockerfile
├─ docker-compose.yml
├─ .dockerignore
├─ .python-version
├─ env.example
└─ README.md
```

## ⚙️ Configuration
Create a `.env` at the project root (see `env.example`):

- Telegram: `TELEGRAM_TOKEN`, `TELEGRAM_CHANNEL_ID`
- Source: `CLONED_PAGE_URL`
- Interval: `CHECK_INTERVAL` (default 10s)
- WhatsApp: `WHATSAPP_AUTH_TOKEN`, `WHATSAPP_RECIPIENT`, optional `WHATSAPP_API_URL`
- MongoDB: `MONGO_URI` (required), `MONGO_DB_NAME` (default `apsit_notifier`), `MONGO_COLLECTION` (default `notification_state`)

Notes:
- Telegram and WhatsApp are independent. Set either or both.
- If neither is set, the bot just updates MongoDB without sending.

## 🚀 Run locally (uv)
```bash
uv sync
uv run main.py
```

## 🐳 Run with Docker
Build and run:
```bash
docker compose up --build -d
```
Logs:
```bash
docker compose logs -f
```

## 🧪 Health and operations
- On start, the bot logs initialization and begins periodic checks.
- Mongo writes log item counts after each successful sync.
- Telegram rate limits are handled with RetryAfter-based backoff.

## 🧰 Troubleshooting
- ❌ Telegram 429: The bot auto-retries with backoff; consider increasing `CHECK_INTERVAL` if bursts are frequent.
- ❌ WhatsApp "Channel not found": Verify `WHATSAPP_AUTH_TOKEN` and `WHATSAPP_RECIPIENT` in Whapi.
- ❌ Mongo not updating: Check `MONGO_URI` network/IP allowlist and credentials; see logs for connection errors.
- 🐳 Build errors with uv: Ensure network access and that Compose uses the updated Dockerfile.

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE).

---
Made with ❤️ and asyncio.

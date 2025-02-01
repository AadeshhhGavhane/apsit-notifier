# APSIT Notification Bot 🤖

A Telegram bot that monitors and forwards notifications from APSIT's website to a Telegram channel and subscribed users. Stay updated with the latest announcements, exam notifications, and more!

## Features ✨

- 🔄 Real-time monitoring of APSIT website
- 📢 Instant notifications in Telegram channel
- 👥 Personal notification subscription system
- 🏷️ Categorized notifications (Exams, Scholarships, Events, etc.)
- 🐳 Docker support for easy deployment
- 🔁 Automatic restart on failure

## Categories Monitored 📋

- Latest Announcements
- Exam Notifications
- Office Notifications
- Scholarship Section
- Application Formats
- Cultural Events
- Technical Clubs
- IEEE & CSI

## Prerequisites 📝

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Telegram Bot Token
- Channel or Group to forward messages

## Environment Variables 🔐

Create a `.env` file with the following variables:

```env
TELEGRAM_TOKEN=your_bot_token
CLONED_PAGE_URL=your_url
CHECK_INTERVAL=10
TELEGRAM_CHANNEL_ID=@yourchannel
```

## Installation & Setup 🚀

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/apsit-notifier-bot.git
cd apsit-notifier-bot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the bot:
```bash
python bot.py
```

### Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose up -d --build
```

2. Check logs:
```bash
docker-compose logs -f
```

## Deployment Guide 📦

1. Set up your VPS
2. Install Docker and Docker Compose
3. Clone this repository
4. Configure your `.env` file
5. Run with Docker Compose

Detailed deployment instructions in our [Deployment Guide](DEPLOYMENT.md)

## Commands 🎮

- `/start` - Subscribe to notifications
- `/stop` - Unsubscribe from notifications

## Contributing 🤝

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author ✍️

Aadesh Gavhane 

---
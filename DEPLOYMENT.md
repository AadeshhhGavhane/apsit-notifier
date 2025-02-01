# DEPLOYMENT.md

# Deployment Guide for APSIT Notification Bot

This guide will walk you through deploying the APSIT Notification Bot on a VPS using Docker.

## Prerequisites

- A VPS running Ubuntu 20.04 or later
- SSH access to your VPS
- A domain name (optional)
- Telegram Bot Token
- Target Telegram Channel/Group ID

## Step 1: Server Setup

1. Update your server:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Install essential packages:
```bash
sudo apt install -y curl git
```

## Step 2: Install Docker and Docker Compose

1. Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

2. Install Docker Compose:
```bash
sudo apt install docker-compose -y
```

3. Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Step 3: Clone and Configure the Project

1. Clone the repository:
```bash
git clone https://github.com/yourusername/apsit-notifier-bot.git
cd apsit-notifier-bot
```

2. Create and configure the environment file:
```bash
cp .env.example .env
nano .env
```

Add your configuration:
```env
TELEGRAM_TOKEN=your_bot_token
CLONED_PAGE_URL=your_url
CHECK_INTERVAL=10
TELEGRAM_CHANNEL_ID=@yourchannel
```

## Step 4: Deploy the Bot

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Check if the container is running:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f
```

## Step 5: Maintenance

### Updating the Bot

1. Pull the latest changes:
```bash
git pull origin main
```

2. Rebuild and restart:
```bash
docker-compose up -d --build
```

### Common Commands

- Stop the bot:
```bash
docker-compose down
```

- Restart the bot:
```bash
docker-compose restart
```

- View logs:
```bash
docker-compose logs -f
```

### Backup

The bot stores data in the `data` directory. To backup:

1. Stop the bot:
```bash
docker-compose down
```

2. Backup the data directory:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

3. Restart the bot:
```bash
docker-compose up -d
```

## Troubleshooting

### Bot Not Starting

1. Check logs:
```bash
docker-compose logs -f
```

2. Verify environment variables:
```bash
docker-compose config
```

### Connection Issues

1. Check if the bot can reach Telegram:
```bash
curl -v https://api.telegram.org
```

2. Verify the bot token:
```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
```

### Data Persistence Issues

1. Check directory permissions:
```bash
ls -la data/
```

2. Ensure the data directory is mounted correctly:
```bash
docker-compose exec bot ls -la /app/data
```

## Security Recommendations

1. Enable UFW (Uncomplicated Firewall):
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

2. Regularly update your system:
```bash
sudo apt update && sudo apt upgrade -y
```

3. Use strong passwords and SSH keys

## Monitoring

To monitor the bot's health:

1. Check container status:
```bash
docker stats
```

2. Monitor system resources:
```bash
htop
```

## Support

If you encounter any issues:

1. Check the logs
2. Review the configuration
3. Open an issue on GitHub
4. Contact the maintainers

import os
from dotenv import load_dotenv
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError
from telegram.helpers import escape_markdown

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "CLONED_PAGE_URL": os.getenv("CLONED_PAGE_URL"),
    "CHECK_INTERVAL": int(os.getenv("CHECK_INTERVAL", "10")),
    "DATA_FILE": "data/notification_data.json",
    "SUBSCRIBERS_FILE": "data/subscribers.json",
    "CHANNEL_ID": os.getenv("TELEGRAM_CHANNEL_ID")
}

class NotificationBot:
    def __init__(self):
        self.application = Application.builder().token(CONFIG["TOKEN"]).build()
        self.session = aiohttp.ClientSession()
        
        # Register command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user_id = update.effective_user.id
        await self.add_subscriber(user_id)
        await update.message.reply_text(
            "👋 Welcome to the Notification Bot!\n\n"
            "I'll keep you updated with the latest notifications.\n"
            "Use /stop to unsubscribe from notifications."
        )

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /stop command"""
        user_id = update.effective_user.id
        await self.remove_subscriber(user_id)
        await update.message.reply_text(
            "You've been unsubscribed from notifications. Use /start to subscribe again."
        )

    async def get_latest_notifications(self):
        try:
            async with self.session.get(CONFIG["CLONED_PAGE_URL"]) as response:
                if response.status == 200:
                    content = await response.text()
                    return self.parse_content(content)
                logger.error(f"HTTP Error: {response.status}")
                return {}
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            return {}

    def parse_content(self, content):
        notifications = {
            "Latest Announcements": [],
            "Exam Notifications": [],
            "Office Notifications": [],
            "Scholarship Section": [],
            "Application Formats": [],
            "Cultural Events": [],
            "Technical Clubs": [],
            "IEEE & CSI": []
        }
        
        # Define sections mapping
        sections_map = {
            "Latest announcements": "Latest Announcements",
            "Exam Notifications": "Exam Notifications",
            "Office Notifications": "Office Notifications",
            "Scholarship Section": "Scholarship Section",
            "Application Formats": "Application Formats",
            "Cultural Events": "Cultural Events",
            "Technical Clubs": "Technical Clubs",
            "IEEE & CSI": "IEEE & CSI"
        }

        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all section blocks
        sections = soup.select('section.block')
        
        for section in sections:
            header = section.find('h2')
            if not header:
                continue
                
            section_title = header.get_text(strip=True)
            section_key = sections_map.get(section_title)

            if not section_key:
                logger.warning(f"Skipping unknown section: {section_title}")
                continue
                
            content_div = section.find('div', class_='content')
            if not content_div:
                continue
                
            # Process content based on section type
            items = []
            if section_key == "Latest Announcements":
                items = content_div.find_all('li', class_='post')
            else:
                items = content_div.find_all(['a', 'li'])

            # Process each item
            for item in items:
                try:
                    # Latest Announcements have special structure
                    if section_key == "Latest Announcements":
                        title = item.find('a').get_text(strip=True)
                        link = item.find('a')['href']
                        date = item.find('div', class_='date').get_text(strip=True)
                        author = item.find('div', class_='name').get_text(strip=True)
                        
                        notifications[section_key].append({
                            "title": self.clean_text(title),
                            "link": link,
                            "date": date,
                            "author": author
                        })
                    else:
                        # Handle regular links
                        if item.name == 'a':
                            title = item.get_text(strip=True)
                            link = item['href']
                        elif item.name == 'li':
                            link = item.find('a')['href']
                            title = item.get_text(strip=True).replace('\n', ' ')
                        else:
                            continue
                            
                        notifications[section_key].append({
                            "title": self.clean_text(title),
                            "link": link
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing item in {section_key}: {str(e)}")
                    continue

        return notifications

    def clean_text(self, text, for_markdown=False):
        """
        Clean text while preserving natural formatting
        """
        if for_markdown:
            markdown_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for char in markdown_chars:
                text = text.replace(char, f"\\{char}")
        else:
            text = text.replace('\\', '')
        
        return " ".join(text.split())

    async def add_subscriber(self, user_id):
        subscribers = self.load_subscribers()
        if user_id not in subscribers["users"]:
            subscribers["users"].append(user_id)
            self.save_subscribers(subscribers)
            logger.info(f"New subscriber: {user_id}")

    async def remove_subscriber(self, user_id):
        subscribers = self.load_subscribers()
        if user_id in subscribers["users"]:
            subscribers["users"].remove(user_id)
            self.save_subscribers(subscribers)
            logger.info(f"Unsubscribed: {user_id}")

    def load_subscribers(self):
        try:
            with open(CONFIG["SUBSCRIBERS_FILE"], "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": []}

    def save_subscribers(self, subscribers):
        os.makedirs(os.path.dirname(CONFIG["SUBSCRIBERS_FILE"]), exist_ok=True)
        with open(CONFIG["SUBSCRIBERS_FILE"], "w") as f:
            json.dump(subscribers, f)

    async def check_for_updates(self):
        current = await self.get_latest_notifications()
        previous = self.load_notification_data()
        new_notifications = self.find_new_notifications(current, previous)
        if new_notifications:
            await self.send_notifications(new_notifications)
            self.save_notification_data(current)

    def find_new_notifications(self, current, previous):
        return {
            section: [item for item in current[section]
                      if item not in previous.get(section, [])]
            for section in current
        }

    async def send_notifications(self, new_notifications):
        # First send to channel if configured
        if CONFIG["CHANNEL_ID"]:
            await self.send_channel_notifications(new_notifications)
        
        # Then send to individual subscribers
        subscribers = self.load_subscribers()
        for user_id in subscribers["users"]:
            await self.send_user_notifications(user_id, new_notifications)

    async def send_channel_notifications(self, notifications):
        """Send notifications to the configured channel"""
        for section, items in notifications.items():
            for item in items:
                try:
                    message = self.format_message(section, item)
                    await self.application.bot.send_message(
                        chat_id=CONFIG["CHANNEL_ID"],
                        text=message,
                        parse_mode=None,
                        disable_web_page_preview=False
                    )
                    await asyncio.sleep(0.5)  # Rate limiting delay
                except TelegramError as e:
                    logger.error(f"Failed to send to channel {CONFIG['CHANNEL_ID']}: {str(e)}")
                    try:
                        simple_message = f"{item['title']}\n{item['link']}"
                        await self.application.bot.send_message(
                            chat_id=CONFIG["CHANNEL_ID"],
                            text=simple_message,
                            parse_mode=None
                        )
                    except TelegramError as e2:
                        logger.error(f"Fallback message also failed for channel: {str(e2)}")

    async def send_user_notifications(self, user_id, notifications):
        for section, items in notifications.items():
            for item in items:
                try:
                    message = self.format_message(section, item)
                    await self.application.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode=None,
                        disable_web_page_preview=False
                    )
                    await asyncio.sleep(0.5)
                except TelegramError as e:
                    logger.error(f"Message failed to {user_id}: {str(e)}")
                    try:
                        simple_message = f"{item['title']}\n{item['link']}"
                        await self.application.bot.send_message(
                            chat_id=user_id,
                            text=simple_message,
                            parse_mode=None
                        )
                    except TelegramError as e2:
                        logger.error(f"Fallback message also failed to {user_id}: {str(e2)}")

    def format_message(self, section, item):
        """Format message with minimal markdown escaping"""
        clean_section = self.clean_text(section, for_markdown=False)
        clean_title = self.clean_text(item['title'], for_markdown=False)
        link = item['link']
        
        base = f"📣 New {clean_section}!\n\n{clean_title}\n🔗 {link}"
        
        if all(key in item for key in ('date', 'author')):
            clean_date = self.clean_text(item['date'], for_markdown=False)
            clean_author = self.clean_text(item['author'], for_markdown=False)
            return f"{base}\n🗓 {clean_date}\n👤 {clean_author}"
        
        return base

    def load_notification_data(self):
        try:
            with open(CONFIG["DATA_FILE"], "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_notification_data(self, data):
        os.makedirs(os.path.dirname(CONFIG["DATA_FILE"]), exist_ok=True)
        with open(CONFIG["DATA_FILE"], "w") as f:
            json.dump(data, f)

    async def show_countdown(self):
        """Display animated countdown in terminal"""
        remaining = CONFIG["CHECK_INTERVAL"]
        try:
            while remaining > 0:
                line = f"⏳ Next fetch in {remaining} sec... (Press Ctrl+C to exit) "
                print(line.ljust(50), end='\r', flush=True)
                await asyncio.sleep(1)
                remaining -= 1
            print(" " * 50, end='\r')
        except asyncio.CancelledError:
            print(" " * 50, end='\r')
            raise

    async def main_loop(self):
        logger.info("Bot started. Press Ctrl+C to stop.")
        while True:
            try:
                await self.check_for_updates()
                await self.show_countdown()
            except Exception as e:
                logger.error(f"Main loop error: {str(e)}")
                await asyncio.sleep(1)

async def main():
    bot = NotificationBot()
    try:
        await bot.application.initialize()
        await bot.application.start()
        await bot.application.updater.start_polling()
        
        await bot.main_loop()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.session.close()
        await bot.application.stop()
        await bot.application.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
import logging

from utils.notification_bot import NotificationBot


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    bot = NotificationBot()
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

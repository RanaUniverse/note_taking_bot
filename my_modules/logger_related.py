import logging

from my_modules import bot_config_settings

# This Below logging i copy paste from teh PTB docs,
# This are used by ptb backend so i dont think to touch this below

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Avoid too much logging from `httpx`
logging.getLogger("httpx").setLevel(logging.WARNING)

# General logger (backend use) so in the main.py i need to import this logger.
logger = logging.getLogger(__name__)


# Below Logics are for making the log for my own beheaviour
# which includes use the my log file name from bot_config_settings module

LOG_FILE_NAME = bot_config_settings.LOG_FILE_NAME


# 🌟 2️⃣ Custom `RanaLogger` for file logging i will think to use.


# from logging.handlers import RotatingFileHandler
# # Use RotatingFileHandler to manage log size & recreation
# file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)


RanaLogger = logging.getLogger("Rana Name")
RanaLogger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    filename=LOG_FILE_NAME,
)

file_handler.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ),
)

RanaLogger.addHandler(file_handler)
RanaLogger.propagate = False  # Prevent console logging

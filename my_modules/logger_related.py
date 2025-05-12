import logging

from my_modules.some_constants import BotSettingsValue


# 🌟 1️⃣ Global logging for backend this need by the PTB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Avoid too much logging from `httpx`
logging.getLogger("httpx").setLevel(logging.WARNING)

# General logger (backend use) so in the main.py i need to import this logger.
logger = logging.getLogger(__name__)


# Below Logics are for making the log for my own beheaviour
# which includes use the my log file name from the .env file


LOG_FILE_NAME = BotSettingsValue.LOG_FILE_NAME.value


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


def main():
    """
    This will for test the log file name form the .env file
    """
    from dotenv import load_dotenv

    load_dotenv()

    RanaLogger.warning("Thsi is made by Rana Universe For Testing")

    logger.warning("This is backend of ptb")


if __name__ == "__main__":
    print("This is my custom logger logics.")
    main()

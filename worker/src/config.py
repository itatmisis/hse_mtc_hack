#!/usr/bin/env python3

import logging
from os import getenv

TELEGRAM_SESSION_TOKEN: str = getenv('TELEGRAM_SESSION_TOKEN')
TELEGRAM_API_ID: int = int(getenv('TELEGRAM_API_ID'))
TELEGRAM_API_HASH: str = getenv('TELEGRAM_API_HASH')
TELEGRAM_MESSAGES_DEFAULT_LIMIT: int = int(getenv("MESSAGES_DEFAULT_LIMIT"), 20)
TELEGRAM_COMMENTS_DEFAULT_LIMIT: int = int(getenv("COMMENTS_DEFAULT_LIMIT"), 20)
TELEGRAM_EXAMPLE_CHANNEL_LINK: str = getenv("EXAMPLE_CHANNEL_LINK", "durov")

API_PORT: int = int(getenv("API_PORT", 80))

# region Logging
# Create a logger instance
log: logging.Logger = logging.getLogger("api.py-worker")

# Create log formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Сreate console logging handler and set its level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

# region Set logging level
logging_level_lower = getenv("LOGGING_LEVEL").lower()
if logging_level_lower == "debug":
    log.setLevel(logging.DEBUG)
    log.critical("Log level set to debug")
elif logging_level_lower == "info":
    log.setLevel(logging.INFO)
    log.critical("Log level set to info")
elif logging_level_lower == "warning":
    log.setLevel(logging.WARNING)
    log.critical("Log level set to warning")
elif logging_level_lower == "error":
    log.setLevel(logging.ERROR)
    log.critical("Log level set to error")
elif logging_level_lower == "critical":
    log.setLevel(logging.CRITICAL)
    log.critical("Log level set to critical")
# endregion
# endregion

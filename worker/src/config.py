#!/usr/bin/env python3

import logging
from os import getenv

telegram_api_id = getenv('TELEGRAM_API_ID')
telegram_api_hash = getenv('TELEGRAM_API_HASH')

# region Logging
# Create a logger instance
log = logging.getLogger("main.py-vkbottle")

# AIOGram logging
# logging.basicConfig(level=logging.DEBUG)

# Create log formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Сreate console logging handler and set its level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

# Create file logging handler and set its level
# fh = logging.FileHandler(r"logs/worker.log")
# fh.setFormatter(formatter)
# log.addHandler(fh)

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

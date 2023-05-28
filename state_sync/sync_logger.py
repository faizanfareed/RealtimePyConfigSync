import logging

from .app_config import LOGGER_NAME, LOGGING_LEVEL

logger = logging.getLogger(LOGGER_NAME)

# Set the default logging level
logger.setLevel(LOGGING_LEVEL)

# Create a handler and add it to the logger
handler = logging.StreamHandler()
logger.addHandler(handler)

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Set the log format
formatter = logging.Formatter(format)
handler.setFormatter(formatter)


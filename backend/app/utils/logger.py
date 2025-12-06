from loguru import logger
from app.config import settings
import sys

logger_config = settings.logger_config

logger.remove()
logger.add(sys.stderr, format=logger_config.FORMAT_LOG, level="INFO")
logger.add(logger_config.LOG_PATH, format=logger_config.FORMAT_LOG, rotation=logger_config.LOG_ROTATION, level="DEBUG")

from app.config import settings 
import sys
from loguru import logger, Logger


log_config = settings.logger_config


def get_logger() -> Logger:
    logger.remove()
    logger.add(log_config.LOG_PATH, 
               rotation=log_config.LOG_ROTATION, 
               format=log_config.FORMAT_LOG,
               level="DEBUG"
    )
    logger.add(sys.stderr, 
               rotation=log_config.LOG_ROTATION, 
               format=log_config.FORMAT_LOG,
               level="INFO"
    )
    return logger

from app.core.config import settings 
import sys
from loguru import logger


log_config = settings.logger_config

def get_logger():
    logger.remove()
    logger.add(log_config.LOG_PATH, 
               rotation=log_config.LOG_ROTATION, 
               format=log_config.FORMAT_LOG,
               level="DEBUG"
    )
    logger.add(sys.stderr, 
               format=log_config.FORMAT_LOG,
               level="INFO"
    )
    return logger


logger = get_logger()

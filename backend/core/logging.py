from loguru import logger
import sys

# Logging setup for the backend service using Loguru.
# Configures log output to stdout with a readable format and INFO level.
# This function should be called at application startup to initialize logging.
def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False,
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                      "<level>{level: <8}</level> | "
                      "{message}")
    return logger

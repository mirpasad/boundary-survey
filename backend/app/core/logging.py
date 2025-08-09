from loguru import logger
import sys

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False,
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                      "<level>{level: <8}</level> | "
                      "{message}")
    return logger

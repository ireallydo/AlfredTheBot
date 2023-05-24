import os
import sys
from datetime import timedelta
from loguru import logger


def setup_logger(settings):
    file_path = "/".join(settings.LOG_FILEPATH.split("/")[:-1])

    try:
        os.makedirs(file_path, exist_ok=True)
    except FileNotFoundError:
        pass  # if passed file path consist only of filename

    logger.remove()

    logger.level("TRACE", color="<fg #BDD9D9><b>")
    logger.level("DEBUG", color="<fg #317DCE><b>")
    logger.level("INFO", color="<fg #9ECDFF><b>")
    logger.level("SUCCESS", color="<b>")
    logger.level("WARNING", color="<fg #00FFFF><b>")
    logger.level("ERROR", color="<fg #FCE94B><b>")
    logger.level("CRITICAL", color="<fg #FF5733><b>")
    log_format = "[{time:YYYY-MM-DD HH:mm:ss ZZ}] [{process}] [<level>{level}</level>] [{name}] {message}"

    logger.add(
        sink=sys.stdout,
        level="TRACE",
        format=log_format
    )
    logger.add(
        sink=settings.LOG_FILEPATH,
        level="TRACE",
        format=log_format,
        rotation=timedelta(days=settings.LOG_ROTATION),
        retention=timedelta(days=settings.LOG_RETENTION)
    )

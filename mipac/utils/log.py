import logging
from typing import Literal

LOGING_LEVEL_TYPE = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOGING_LEVELS = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


def setup_logging(
    *,
    handler: logging.Handler | None = None,
    formatter: logging.Formatter | None = None,
    level: LOGING_LEVEL_TYPE = "INFO",
) -> None:
    if level not in LOGING_LEVELS:
        raise Exception(f"Not found logging level {level}")
    _level = LOGING_LEVELS[level]

    if handler is None:
        handler = logging.StreamHandler()

    if formatter is None:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(_level)
    logger.addHandler(handler)

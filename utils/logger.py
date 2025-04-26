import logging
from rich.logging import RichHandler
from uvicorn.logging import DefaultFormatter

FORMAT = "%(asctime)s %(funcName) -25s %(lineno) -4d: %(message)s"


def get_logger(name: str = None):
    """Create a logger"""
    logging.basicConfig(
        level="NOTSET", format=FORMAT, handlers=[RichHandler("DEBUG", show_time=False)]
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = DefaultFormatter(FORMAT, use_colors=True)
    if logger.hasHandlers():
        for handle in logger.handlers:
            handle.setFormatter(formatter)
    else:
        handle = RichHandler("DEBUG")
        logger.addHandler(handle)
    # add ch to logger
    return logger

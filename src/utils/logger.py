from logging import INFO, Formatter, StreamHandler, getLogger
from sys import stdout


def setup_log():
    uvicorn_access_logger = getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = []
    uvicorn_access_logger.propagate = False

    uvicorn_error_logger = getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = []
    uvicorn_error_logger.propagate = False

    root_logger = getLogger()
    root_logger.setLevel(INFO)
    ch = StreamHandler(stdout)
    ch.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(ch)


def info(*kwargs):
    return getLogger(__name__).info(*kwargs)


def error(*kwargs):
    return getLogger(__name__).error(*kwargs)


def debug(*kwargs):
    return getLogger(__name__).debug(*kwargs)


def warning(*kwargs):
    return getLogger(__name__).warning(*kwargs)


def critical(*kwargs):
    return getLogger(__name__).critical(*kwargs)

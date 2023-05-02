import logging
import os

LOG_NAME = "utparking"


class CustomFormatter(logging.Formatter):
    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[41;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] %(levelname)8s: %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger():
    log = logging.getLogger(LOG_NAME)
    log.propagate = False
    log.setLevel(logging.DEBUG)
    add_stream_handler(log)
    return log


def add_stream_handler(log: logging.Logger):
    for handler in log.handlers:
        if isinstance(handler, logging.StreamHandler):
            return
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    log.addHandler(ch)


def config_logger(cfg):
    log = get_logger()
    formatter = logging.Formatter(
        "[%(asctime)s][%(pathname)s:%(lineno)d] %(levelname)s: %(message)s")
    if "log_dir" in vars(cfg):
        fh = logging.FileHandler(os.path.join(cfg.log_dir, "log.txt"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    add_stream_handler(log)

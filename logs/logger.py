# logger.py
from os import path
from time import monotonic_ns as timing_point
import logging

LOGS_DIR = path.dirname(path.abspath(__file__))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{path.join(LOGS_DIR, "log.txt")}")
             ]
                    )

def function_log(func):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        t0 = timing_point()
        logger.info(f"{(func.__module__).upper()}-{func.__name__}: Started.")
        result = func(*args, **kwargs)
        t1 = timing_point()
        logger.info(f"{(func.__module__).upper()}-{(func.__name__)}: Finished in {(t1-t0)/1_000_000_000:.2f} seconds.")
        return result
    return wrapper

logger = logging.getLogger(__name__)
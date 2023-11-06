import time
import logging

logging.basicConfig(filename='timing.log', level=logging.INFO)

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.6f} seconds to execute.")
        logging.info(f"{func.__name__} took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper



import threading
from functools import wraps

from .objects import ResultCatcher


def timeout(duration):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret_val = ResultCatcher(func)
            th = threading.Thread(target=ret_val, args=args, kwargs=kwargs)
            th.start()
            th.join(duration)
            if th.is_alive():
                raise TimeoutError(
                    "Function took longer than {} seconds, function: {}".format(duration, func.__name__))
            else:
                return ret_val.val
        return wrapper
    return decorator

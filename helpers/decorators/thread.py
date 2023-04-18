import threading
from functools import wraps

from .objects import ResultCatcher

def thread(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        ret_val = ResultCatcher(func)
        th = threading.Thread(target=ret_val, args=args, kwargs=kwargs)
        th.start()
        th.join()
        return ret_val.val
    return decorator
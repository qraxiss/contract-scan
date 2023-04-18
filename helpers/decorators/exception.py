from logging import error, basicConfig, ERROR
from datetime import datetime as dt
from traceback import format_exc
from functools import wraps
from time import sleep

basicConfig(filename=f'log/error/error.log', level=ERROR)
line = "---------------------------------------------------------------------------"

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            error(f'{line}\ndatetime: "{str(dt.now())}"\n{format_exc()}')
    return inner_function


from time import sleep
def retry(path: str, max_attempts: int = 0, forever: bool = False):
    basicConfig(filename=path, level=ERROR)
    def inner(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while forever or (attempt < max_attempts):
                sleep(1)
                attempt += 1
                try:
                    return func(*args, **kwargs)
                except:
                    error(f'{line}\ndatetime: "{str(dt.now())}"\n{format_exc()}')
        return wrapper
    return inner
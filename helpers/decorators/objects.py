class ResultCatcher:
    def __init__(self, func):
        self.func = func
        self.val = None

    def __call__(self, *args, **kwargs):
        self.val = self.func(*args, **kwargs)
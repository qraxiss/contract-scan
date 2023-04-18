from collections import defaultdict

import inspect
import concurrent

from .generator import Generator

from .utils import *
from helpers import exception_handler


from random import choice
from time import sleep

class Checker(Telegram, Twitter, Site, LinkTree, GitBook, GitHub, Medium, EthScan):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.count = 0
        self.collects = defaultdict(list)
        self.range = range(1,5)
        #Request Decorator
        request_methods_str = ['telegram', '_site', 'twitter',
                               'medium', 'linktree', 'gitbook',
                               'github']
        request_methods = [getattr(self, method)
                           for method in request_methods_str]

        for name, func in zip(request_methods_str, request_methods):
            setattr(self, name, self.response(func))

# https://mainnet.infura.io/v3/ee29d3ce90f9450fb3dd7e667d70654e
        # Exception Handing Decorator
        # for name, func in inspect.getmembers(self, inspect.ismethod):
        #     setattr(self, name, exception_handler(func))


    def response(self, func):
        def inner_function(*args, **kwargs):
            #sleep(choice(self.range))
            method, username, result, status = func(*args, **kwargs)

            self.count += 1

            if result == True:
                self._saver(method, username)

            data = [str(i) for i in [self.count, method, username, result, status]]
            self._log(",".join(data))
            #return data

        return inner_function

    def _check(self, method, name) -> list:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = {username: executor.submit(
                method, username) for username in self.check_list[name]}
            concurrent.futures.wait(results.values())

        return self.collects[name]

    def check__(self):
        self.collects = defaultdict(list)
        checker_list =  {name: getattr(self, name)  for name in self.social_medias}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = {name: executor.submit(self._check, method, name) for name, method in checker_list.items()}
            concurrent.futures.wait(results.values())

    
    def check(self, socials = None):
        if not socials:
            socials = self.social_medias
        self.collects = defaultdict(list)
        checker_list =  {name: getattr(self, name)  for name in socials}
        for name, method in checker_list.items():
            self._check(method, name)

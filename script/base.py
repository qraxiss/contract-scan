from collections import defaultdict
from requests import get
import datetime

# https://mainnet.infura.io/v3/ee29d3ce90f9450fb3dd7e667d70654e

from .generator import Generator

class CheckByResponse(Generator):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    collects = defaultdict(list)

    url = {
        'site': lambda site: site,
        'github': lambda username: f"https://github.com/{username}",
        'linktree': lambda username: f"https://linktr.ee/{username}",
        'medium': lambda username: f"https://medium.com/@{username}",
        'ethscan': lambda contract: f"https://etherscan.io/token/{contract}",
        'gitbook': lambda username: f"https://{username}.gitbook.io",
        'twitter': lambda username: f"https://twitter.com/{username}",
        'telegram': lambda username: f"https://t.me/{username}"
    }

    def __init__(self, info: dict) -> None:
        super().__init__(info)
        self.check_list = self.combinations
        now = datetime.datetime.now()
        self.fp = open(f'log/res/{now}.log', 'a+')
        self.fp.write('index,site,nick,social,status\n')
        
    @classmethod
    def get(cls, url, *args, **kwargs): 
        return get(headers=cls.headers, url=url, timeout=1, *args, **kwargs)

    @classmethod
    def apiget(cls, url, *args, **kwargs):
        return get(url=url, timeout = 1, *args, **kwargs)

    def _log(self, data):
        self.fp.write(data + "\n")

    def _req(self, site, page):
        url = self.url[site](page)
        res = self.get(url)
        return res

    def _check_res_type(self, site, page) -> bool:
        res = self._req(site, page)
        return [res.status_code == 200, res.status_code]

    def _check_contains(self, site, page, string) -> bool:
        res = self._req(site, page)
        return [not string in res.text, res.status_code]


    def _saver(self, site: str, value: dict) -> None:
        self.collects[site].append(value)
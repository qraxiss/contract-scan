from helpers import ListHashableDict, timeout
import concurrent.futures
import datetime
import inspect
import whois

from ..base import CheckByResponse

from requests.exceptions import ConnectionError as SiteNotFound
from requests import get

class Site(CheckByResponse):
    exts = ['com',
            'net',
            'org',
            'biz',
            'info',
            'pro',
            'io',
            'finance',
            'tech',
            'app',
            'xyz',
            'space',
            'site']
    query_dt = datetime.datetime.now() - datetime.timedelta(days=30*4)

    def site(self, username):
        urls = tuple(map(lambda ext: f'{username}.{ext}', self.exts))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = {username: executor.submit(
                self._site, url) for url in urls}
            concurrent.futures.wait(results.values())

        return self.collects['site']

    def _site(self, url):
        method = inspect.stack()[0][3].replace('_', '')
        result = self.__site(url)

        return [method, url, result, None]

    def __site(self, url):
        try:
            res = get(f'http://{url}', timeout=5)
        except SiteNotFound:
            return False
        except Exception as e:
            return e
        else:
            date = whois.whois(url)['creation_date']
            try:
                return date >= self.query_dt
            except:
                return min(date) >= self.query_dt

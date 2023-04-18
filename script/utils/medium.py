import inspect

from ..base import CheckByResponse

class Medium(CheckByResponse):
    def medium(self, username):
        method = inspect.stack()[0][3]
        result, status = self._check_contains(method, username, '404')
        return method, username, result, status
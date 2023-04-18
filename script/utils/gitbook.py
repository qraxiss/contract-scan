import inspect

from ..base import CheckByResponse

class GitBook(CheckByResponse):
    def gitbook(self, username):
        method = inspect.stack()[0][3]
        result, status = self._check_res_type(method, username)
        return method, username, result, status
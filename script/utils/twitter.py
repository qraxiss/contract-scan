from ..base import CheckByResponse
import inspect
import tweepy


class Twitter(CheckByResponse):
    api_key = "lrRyeX5pooupcrrJQfhK3T4tX"
    api_secret = "clg0z6cP3caBTUOoOOcoXjWkSnhNYaAMONHvw7PBqCmPQhb7cn"
    access = "1303011872657100803-BCWtDXtS2nqzr4qAwLi1GrcBtAriII"
    access_secret = "R7mhWgG7TqkQOAi95sa2mqgEGxieNniR1hgMB0gzPeVWf"

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access, access_secret)
    api = tweepy.API(auth, timeout=2)

    def twitter(self, username):
        method = inspect.stack()[0][3].replace('_', '')
        try:
            account = self.api.get_user(screen_name=username)
        except Exception as e:
            result = e
        else:
            result = True

        return method, username, result, None

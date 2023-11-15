import requests
from app_settings.models import AppSettings


class Poster:

    url = 'https://joinposter.com'

    def get(self, url, params=None, **kwargs):
        self.url += url
        token_value = AppSettings.poster_token.get().value
        params.update({'token': token_value})
        return requests.get(url=self.url, params=params, **kwargs)

import base64

from couchpotato.core.event import addEvent
from couchpotato.core.helpers.variable import sha1
from couchpotato.core.logger import CPLog
from couchpotato.core.media.movie.providers.automation.base import Automation


log = CPLog(__name__)

autoload = 'Trakt'


class Trakt(Automation):

    urls = {
        'base': 'http://api.trakt.tv/',
        'watchlist': 'user/watchlist/movies.json/%s/',
    }

    def __init__(self):
        super(Trakt, self).__init__()

        addEvent('setting.save.trakt.automation_password', self.sha1Password)

    def sha1Password(self, value):
        return sha1(value) if value else ''

    def getIMDBids(self):

        return [movie.get('imdb_id') for movie in self.getWatchlist()]

    def getWatchlist(self):
        method = (self.urls['watchlist'] % self.conf('automation_api_key')) + self.conf('automation_username')
        return self.call(method)

    def call(self, method_url):

        headers = {}
        if self.conf('automation_password'):
            headers[
                'Authorization'
            ] = f"""Basic {base64.encodestring(f"{self.conf('automation_username')}:{self.conf('automation_password')}")[:-1]}"""


        data = self.getJsonData(self.urls['base'] + method_url, headers = headers)
        return data or []


config = [{
    'name': 'trakt',
    'groups': [
        {
            'tab': 'automation',
            'list': 'watchlist_providers',
            'name': 'trakt_automation',
            'label': 'Trakt',
            'description': 'import movies from your own watchlist',
            'options': [
                {
                    'name': 'automation_enabled',
                    'default': False,
                    'type': 'enabler',
                },
                {
                    'name': 'automation_api_key',
                    'label': 'Apikey',
                },
                {
                    'name': 'automation_username',
                    'label': 'Username',
                },
                {
                    'name': 'automation_password',
                    'label': 'Password',
                    'type': 'password',
                    'description': 'When you have "Protect my data" checked <a href="http://trakt.tv/settings/account">on trakt</a>.',
                },
            ],
        },
    ],
}]

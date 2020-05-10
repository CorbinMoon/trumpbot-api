import requests
import json
import base64


OAUTH_ENDPOINT = 'https://api.twitter.com/oauth2/token'
TWITTER_SEARCH = 'https://api.twitter.com/1.1/search/tweets.json?q={}&count={}&lang=en'


class TwitterClient:

    def __init__(self, creds):
        self._creds_string = self.get_creds_string(creds)
        self._access_token = self.get_bearer_token()

    @classmethod
    def get_creds_string(cls, creds):
        s = '{}:{}'.format(creds['key'], creds['secret'])
        s = base64.urlsafe_b64encode(s.encode('utf-8'))
        return str(s, 'utf-8')

    def get_bearer_token(self):
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Basic ' + self._creds_string
        }

        resp = requests.post(url=OAUTH_ENDPOINT,
                             data=data,
                             headers=headers)
        resp_json = json.loads(resp.content)
        return resp_json['access_token']

    def query(self, s, count=10):
        headers = {
            'Authorization': 'Bearer ' + self._access_token
        }

        resp = requests.get(url=TWITTER_SEARCH.format(s, count),
                            headers=headers)
        return json.loads(resp.content)

    def query_for_text(self, s, count=10):
        tweets = self.query(s, count)['statuses']
        return [tweet['text'] for tweet in tweets]

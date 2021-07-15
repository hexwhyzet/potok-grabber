import requests

if __name__ == '__main__':
    from config import Secrets, Config
else:
    from grabber_reddit.config import Secrets, Config

secrets = Secrets()
config = Config()

CLIENT_ID = config["reddit_client_id"]
SECRET_KEY = secrets["reddit_secret_key"]
ACCESS_TOKEN = secrets["reddit_access_token"]
USER_AGENT = "MyAPI/0.0.1"


def get_access_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': 'potokdevelopers',
        'password': 'xY85dZQA5cF6kU5huWbp',
    }
    headers = {'User-Agent': USER_AGENT}
    token = requests.post('https://www.reddit.com/api/v1/access_token',
                          auth=auth, data=data, headers=headers).json()['access_token']
    return token


def reddit_api_request(method, params=None):
    if params is None:
        params = dict()
    headers = {'User-Agent': USER_AGENT, **{'Authorization': f'bearer {get_access_token()}'}}
    response = requests.get(f"https://oauth.reddit.com/{method}", params=params, headers=headers).json()
    return response


if __name__ == '__main__':
    print(get_access_token())

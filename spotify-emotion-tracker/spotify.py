import requests
import json

auth = dict()
with open('auth.json', 'r') as f:
    auth = json.load(f)


def get_auth_header(token):
    return {
        'Authorization': f'Bearer {token}'
    }


def get_token(code):
    body = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': auth.get('redirect_uri'),
            'client_id': auth.get('client_id'),
            'client_secret': auth.get('client_secret')}
    r = requests.post(
        'https://accounts.spotify.com/api/token',
        data=body)
    return r.json().get('access_token')


def authorize():
    link = 'https://accounts.spotify.com/authorize?response_type=code&client_id={}&scope={}&redirect_uri={}'\
        .format(auth.get('client_id'),
                auth.get('scope'),
                auth.get('redirect_uri'))
    return link


def get_audio_features(token, id):
    r = requests.get(
        f'https://api.spotify.com/v1/audio-features/{id}',
        headers=get_auth_header(token)
    )
    return r


def get_many_audio_features(token, ids):
    q = ','.join(ids)
    r = requests.get(
        f'https://api.spotify.com/v1/audio-features/?ids={q}',
        headers=get_auth_header(token)
    )
    return r


def get_playlist_tracks(token, id):
    r = requests.get(
        f'https://api.spotify.com/v1/playlists/{id}/tracks',
        headers=get_auth_header(token)
    )
    return r

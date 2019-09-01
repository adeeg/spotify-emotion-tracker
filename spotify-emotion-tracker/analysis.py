from .spotify import get_playlist_tracks, get_many_audio_features
from collections import defaultdict


def combine_responses(responses):
    items = []
    for r in responses:
        items.extend(r.json().get('items'))
    return {'items': items}


def analyse_playlist(token, id):
    playlist_responses = get_playlist_tracks(token, id)

    playlist_info = combine_responses(playlist_responses)

    # chunk playlist
    tracks = playlist_info.get('items')
    ids = [x.get('track').get('id') for x in tracks]
    chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]

    # get all valences
    r = 'none'
    valences = []
    dates = [x.get('added_at') for x in tracks]
    for chunk in chunks:
        r = get_many_audio_features(token, chunk).json().get('audio_features')
        valences.extend([x.get('valence') for x in r])
    return dates, valences


def group_by_day(dates, valences):
    dates_new = []
    valences_new = []
    d = defaultdict(list)

    for x in zip(dates, valences):
        d[x[0]] += [x[1]]
    for k, v in d.items():
        dates_new.append(k)
        valences_new.append(sum(v) / len(v))
    return dates_new, valences_new


def group_by_week(dates, valences):
    pass

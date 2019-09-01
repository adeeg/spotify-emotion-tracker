from .spotify import get_playlist_tracks, get_many_audio_features


def analyse_playlist(token):
    playlist_info = get_playlist_tracks(token, '4V9zwfRVcVyGmaqtktCGfD')

    # chunk playlist
    tracks = playlist_info.json().get('items')
    ids = [x.get('track').get('id') for x in tracks]
    chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]

    # get all valences
    r = 'none'
    valences = []
    for chunk in chunks:
        r = get_many_audio_features(token, chunk)
        v = [x.get('valence')
             for x in r.json().get('audio_features')]
        valences.extend(v)
    return str(valences)

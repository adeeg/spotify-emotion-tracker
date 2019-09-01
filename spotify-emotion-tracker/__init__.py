from flask import Flask, request, redirect, url_for
import requests
import json
from .spotify import get_token, authorize, get_audio_features
from .analysis import analyse_playlist


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        code = request.args.get('code')

        if code:
            # we have a token
            token = get_token(code)
            # feat = get_audio_features(
            #     token,
            #     '5w3yxRRxy5pvZdUvBJF6ve')
            r = analyse_playlist(token)

            return r
        else:
            # get a token
            return redirect(url_for('authorization'))

    @app.route('/authorization')
    def authorization():
        return redirect(authorize())

    return app

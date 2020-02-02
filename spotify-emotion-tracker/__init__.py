#!/usr/bin/python3

from flask import Flask, request, redirect, url_for, render_template
import requests
import json
from .spotify import get_token, authorize, get_audio_features, get_user, get_user_playlists
from .analysis import analyse_playlist, group_by_day


def create_app(test_config=None):
    app = Flask(__name__,
                static_folder='../dist/static',
                template_folder='../dist')

    """ @app.route('/')
    def index():
        token = request.args.get('token')
        if token:
            # we have a token
            user_id = get_user(token).json().get('id')
            playlists = get_user_playlists(token, user_id).json().get('items')
            # eturn render_template('index.html', playlists=json.dumps(playlists))
            return render_template('index.html')
        else:
            # get a token
            return redirect(url_for('authorization')) """

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyse')
    def analyse():
        token = request.args.get('token')
        id = request.args.get('id')

        if token:
            r = analyse_playlist(token, id)

            # remove time from date
            dates = [x[:10] for x in r[0]]
            dates, valences = group_by_day(dates, r[1])

            return render_template('analyse.html', labels=json.dumps(dates), data=valences)
        else:
            return redirect(url_for('authorization'))

    @app.route('/authorization')
    def authorization():
        return redirect(authorize())

    @app.route('/token')
    def token():
        code = request.args.get('code')
        if code:
            token = get_token(code)
        else:
            return redirect(url_for('authorization'))
        return redirect(url_for('index', token=token))

    return app

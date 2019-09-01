init:
	pipenv install
server:
	export FLASK_APP=spotify-emotion-tracker && flask run
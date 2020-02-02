init:
	pipenv install
server:
	export FLASK_APP=spotify-emotion-tracker && pipenv run flask run

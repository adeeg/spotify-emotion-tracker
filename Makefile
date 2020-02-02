init:
	pipenv install
build:
	npm run build
server:
	export FLASK_APP=spotify-emotion-tracker && pipenv run flask run

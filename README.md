# spotify-emotion-tracker

## Installing

1. Create `auth.json`:
    ```
    {
    "username": "",
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "http://127.0.0.1:5000/",
    "scope": "user-read-private"
    }
    ```
2. `pipenv install`
3. `make server`
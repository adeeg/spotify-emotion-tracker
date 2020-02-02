# spotify-emotion-tracker

## Installing

1. `pipenv install`
1. `npm install`
1. create `auth.json`:
    ```
    {
        "username": "",
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "http://127.0.0.1:5000/",
        "scope": "user-read-private"
    }
    ```

## Building

`npm run build`


## Running

`make server`

---

## TODO

Design

[ ] enter playlist url instead of id
[x] add song info to graph nodes
[ ] add dropdown button for playlist section

Content

[ ] add 'post to social media' button
[ ] add more options for graph customisation
[ ] add about section

Fixes

[ ] fix profile picture not showing
[ ] fix site redirect
[ ] actually log out
[ ] fix text clipping on playlist names
[ ] delete old code
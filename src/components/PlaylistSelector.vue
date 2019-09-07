<template>
  <div class="container">
    <div>
      <router-link to="/">
        <b-button class="float-left mb-3">Back</b-button>
      </router-link>
    </div>
    <div>
      <b-input-group prepend="Enter a playlist ID:">
        <b-input id="form-input-playlist-id" placeholder="37i9dQZF1DWWQRwui0ExPn"></b-input>
      </b-input-group>
      <hr />
    </div>
    <div>
      <h2>Choose one of your playlists:</h2>
      <b-card
        title="My favourite playlist!!"
        img-src="../assets/spotify_demo_album.jpg"
        img-alt="Album art"
        img-top
        style="max-width: 20rem;"
      >
        <b-card-text>Playlist details</b-card-text>
      </b-card>
    </div>
  </div>
</template>
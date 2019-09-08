<template>
  <div class="container">
    <!-- user info -->
    <b-card
      :title="userInfo.data.display_name"
      :img-src="getUserImage"
      img-alt="Profile picture"
      img-left
    >
      <b-button v-on:click="logout">Log out</b-button>
    </b-card>
    <hr />

    <!-- manual playlist id -->
    <div>
      <b-input-group prepend="Enter a playlist ID:">
        <b-input id="form-input-playlist-id" placeholder="37i9dQZF1DWWQRwui0ExPn"></b-input>
      </b-input-group>
    </div>

    <br />

    <!-- user playlists -->
    <div>
      <h5>Or choose one of your playlists:</h5>

      <div v-if="loadingPlaylists">
        <b-spinner label="Loading..."></b-spinner>
      </div>
      <div v-else>
        <div v-if="badPlaylists">
          <b-alert show variant="danger">Could not load playlists - please try reloading the page.</b-alert>
        </div>
        <div v-else>
          <div v-for="item in userPlaylists.data.items">
            <b-card
              v-bind:key="item.id"
              :img-src="item.images[0].url"
              img-alt="Album art"
              img-left
              img-height="64px"
              img-width="64px"
              style="object-fit: cover;"
            >
              <b-card-text>{{ item.name }}</b-card-text>
            </b-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["userInfo", "token", "getSpotifyAuthHeader"],

  computed: {
    getUserImage: function() {
      return this.userInfo.data.images[0].url;
    }
  },

  data() {
    return {
      userPlaylists: {},
      loadingPlaylists: true,
      badPlaylists: false
    };
  },

  methods: {
    logout: function(event) {
      this.$router.replace({ query: {} });
    },

    getSpotifyPlaylists: function(token) {
      if (token) {
        axios
          .get(`https://api.spotify.com/v1/me/playlists?limit=50`, {
            headers: this.getSpotifyAuthHeader(token)
          })
          .then(response => (this.userPlaylists = response))
          .catch(error => {
            this.badPlaylists = true;
          })
          .finally(() => {
            this.loadingPlaylists = false;
          });
      }
    }
  },

  mounted() {
    this.getSpotifyPlaylists(this.token);
  }
};
</script>
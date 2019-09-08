<template>
  <div class="container">
    <h1>Spotify Emotion Tracker</h1>

    <!-- info after loading user info -->
    <div v-if="this.$route.query.token">
      <div v-if="loadingUserInfo">
        <b-spinner label="Loading..."></b-spinner>
      </div>
      <div v-else>
        <div v-if="badUserInfo">
          <b-alert show variant="danger">Invalid Spotify token - please log in again.</b-alert>
        </div>
        <div v-else>
          <User :token="token" :userInfo="userInfo" :getSpotifyAuthHeader="getSpotifyAuthHeader" />
        </div>
      </div>
    </div>

    <!-- show login button if required -->
    <div v-if="!this.$route.query.token || badUserInfo">
      <a href="authorization">
        <b-button>
          <img
            class="button-spotify-login"
            alt="Spotify logo"
            src="../assets/spotify_icon_white.png"
            height="20px"
          />
          Log in to Spotify
        </b-button>
      </a>
    </div>
  </div>
</template>

<style>
.button-spotify-login {
  margin-right: 7px;
}
</style>

<script>
import axios from "axios";

import User from "./User.vue";

export default {
  components: {
    User
  },

  data() {
    return {
      userInfo: {},
      loadingUserInfo: true,
      badUserInfo: false
    };
  },

  computed: {
    token: function() {
      return this.$route.query.token;
    }
  },

  methods: {
    getSpotifyAuthHeader: function(token) {
      return {
        Authorization: "Bearer " + token
      };
    },

    getSpotifyUserInfo: function(token) {
      if (token) {
        axios
          .get("https://api.spotify.com/v1/me", {
            headers: this.getSpotifyAuthHeader(token)
          })
          .then(response => (this.userInfo = response))
          .catch(error => {
            this.badUserInfo = true;
          })
          .finally(() => {
            this.loadingUserInfo = false;
          });
      }
    }
  },

  beforeCreate() {
    // fix for query being before #
    if (location.search) {
      location.replace(location.pathname + location.hash + location.search);
    }
  },

  mounted() {
    // get user info from spotify
    this.getSpotifyUserInfo(this.token);
  }
};
</script>
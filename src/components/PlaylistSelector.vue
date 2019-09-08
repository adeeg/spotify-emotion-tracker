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

    <!-- user playlists -->
    <div>
      <h3>Or choose one of your playlists:</h3>
      <b-card
        title="My favourite playlist!!"
        img-src="../assets/spotify_demo_album.jpg"
        img-alt="Album art"
        img-left
        style="max-width: 20rem;"
      >
        <b-card-text>Playlist details</b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  /* getSpotifyHeader() {
    return {
      Authorization: 'Bearer '
    }
  } */

  props: ["userInfo"],

  computed: {
    getUserImage: function() {
      return this.userInfo.data.images[0].url;
    }
  },

  data() {
    /* return {
      userInfo: { id: "dog" }
    }; */
  },

  methods: {
    logout: function(event) {
      this.$router.replace({ query: {} });
    }
  },

  mounted() {
    /* axios.get("").then(repose => (this.userInfo = response)); */
  }
};
</script>
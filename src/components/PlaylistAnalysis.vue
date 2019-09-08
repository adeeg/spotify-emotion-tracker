<template>
  <div>
    <div>{{ badTracks }}</div>
    <div>{{ tracksInfo.length }}</div>
    <div>{{ loadingTracks }}</div>
  </div>
</template>
<style>
</style>
<script>
import axios from "axios";

export default {
  props: ["playlistInfo", "token", "getSpotifyAuthHeader"],

  data() {
    return {
      tracksInfo: [],
      badTracks: false,
      loadingTracks: true
    };
  },

  methods: {
    getSpotifyPlaylistTracks: function(token, playlistId, offset) {
      axios
        .get(
          `https://api.spotify.com/v1/playlists/${playlistId}/tracks?offset=${offset}`,
          {
            headers: this.getSpotifyAuthHeader(token)
          }
        )
        .then(response => {
          this.tracksInfo.push(...response.data.items);
          if (response.data.next) {
            this.getSpotifyPlaylistTracks(token, playlistId, offset + 100);
          }
        })
        .catch(error => {
          this.badTracks = true;
        })
        .finally(() => {
          this.loadingPlaylists = false;
        });
    },

    load: function() {
      this.getSpotifyPlaylistTracks(this.token, this.playlistInfo.id, 0);
    }
  },

  mounted() {
    /* this.getSpotifyPlaylistTracks(this.token, this.playlistInfo.id); */
  }
};
</script>
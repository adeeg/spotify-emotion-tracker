<template>
  <div>
    {{ asdf }}
    <div v-if="badTracks">
      <b-alert show variant="danger">Could get tracks from playlist.</b-alert>
      <b-button v-on:click="load">Try to load tracks again</b-button>
    </div>
    <div v-else>
      <div v-if="loading">
        <b-spinner label="Loading..."></b-spinner>
        <div>{{ audioFeatures }}</div>
      </div>
      <div v-else>
        <div>{{ tracksInfo.length }}</div>
        <div>{{ audioFeatures.length }}</div>
      </div>
    </div>
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
      audioFeatures: [],
      badTracks: false,
      loading: true
    };
  },

  methods: {
    getSpotifyPlaylistTracks: function(token, playlistId, offset) {
      return axios
        .get(
          `https://api.spotify.com/v1/playlists/${playlistId}/tracks?offset=${offset}`,
          {
            headers: this.getSpotifyAuthHeader(token)
          }
        )
        .then(response => {
          this.tracksInfo.push(...response.data.items);

          // download this set of audio features
          this.getSpotifyAudioFeatures(
            token,
            response.data.items
              .map(x => x.track.id)
              .reduce((acc, x) => acc + "," + x)
          );

          if (response.data.next) {
            this.getSpotifyPlaylistTracks(token, playlistId, offset + 100);
          } else {
            this.loading = false;
          }
        })
        .catch(error => {
          this.badTracks = true;
        });
    },

    getSpotifyAudioFeatures: function(token, trackIds) {
      axios
        .get(`https://api.spotify.com/v1/audio-features/?ids=${trackIds}`, {
          headers: this.getSpotifyAuthHeader(token)
        })
        .then(response => {
          this.audioFeatures.push(...response.data.audio_features);
        })
        .catch(error => {
          this.badTracks = true;
        });
    },

    load: function() {
      this.getSpotifyPlaylistTracks(this.token, this.playlistInfo.id, 0);
    }
  }
};
</script>
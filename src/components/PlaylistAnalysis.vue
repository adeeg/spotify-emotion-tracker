<template>
  <div>
    {{ asdf }}
    <div v-if="badTracks">
      <b-alert show variant="danger">Could get tracks from playlist.</b-alert>
      <b-button v-on:click="load">Try to load tracks again</b-button>
    </div>
    <div v-else>
      <div v-if="fullyLoaded">
        <FeatureGraph
          :playlistId="playlistInfo.id"
          :tracksInfo="tracksInfo"
          :tracksFeatures="tracksFeatures"
          :optionGroup="optionGroup"
          :key="optionGroup"
        />
        <span>
          <b-form inline>
            <label>Group by </label>
            <b-form-select class="ml-2" v-model="optionGroup" :options="[
                { value: null, text: 'None' },
                { value: 'day', text: 'Day' },
                { value: 'week', text: 'Week' },
                { value: 'month', text: 'Month' }
              ]"><b-form-select/>
          </b-form>
        </span>
      </div>
      <div v-else>
        <b-spinner label="Loading..."></b-spinner>
      </div>
    </div>
  </div>
</template>
<style>
</style>
<script>
import axios from "axios";
import FeatureGraph from "./FeatureGraph.vue";

export default {
  props: ["playlistInfo", "token", "getSpotifyAuthHeader"],

  components: {
    FeatureGraph
  },

  data() {
    return {
      tracksInfo: [],
      tracksFeatures: [],
      badTracks: false,
      loading: true,
      optionGroup: null
    };
  },

  computed: {
    fullyLoaded: function() {
      return (
        !this.loading && this.tracksInfo.length === this.tracksFeatures.length
      );
    }
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
      return axios
        .get(`https://api.spotify.com/v1/audio-features/?ids=${trackIds}`, {
          headers: this.getSpotifyAuthHeader(token)
        })
        .then(response => {
          this.tracksFeatures.push(...response.data.audio_features);
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
<template>
  <div>
    <p>Average happiness: {{ average }}</p>
    <canvas :id="'chart-' + playlistId" width="400" height="400"></canvas>
  </div>
</template>

<style>
</style>

<script>
import Chart from "chart.js";
import moment from "moment";

export default {
  props: ["playlistId", "tracksInfo", "tracksFeatures", "optionGroup"],

  computed: {
    average: function() {
      return (
        this.tracksFeatures.reduce((a, b) => a + b.valence, 0) /
        this.tracksFeatures.length
      );
    }
  },

  methods: {
    getGroupFormat: function(groupMethod, date) {
      switch (groupMethod) {
        case "day":
          return moment(date).format("Do MMM YYYY");
        case "week":
          return moment(date)
            .startOf("week")
            .format("Do MMM YYYY");
        case "month":
          return moment(date).format("MMM YYYY");
        default:
          return moment(date).format("Do MMM YYYY");
      }
      return moment(date).format("Do MMM YYYY");
    },

    // this relies on dates & features being the same length (hopeful x)
    group: function(groupMethod, dates, valences) {
      let dict = {};

      // group together into dict
      for (let i = 0; i < dates.length; i++) {
        let date = dates[i];
        let valence = valences[i];

        let key = this.getGroupFormat(groupMethod, date);

        if (key in dict) {
          dict[key].push(valence);
        } else {
          dict[key] = [valence];
        }
      }
      // reduce valences (avg)
      let newValences = [];
      for (const vals of Object.values(dict)) {
        let mean = vals.reduce((a, b) => a + b, 0) / vals.length;
        newValences.push(mean);
      }

      return [Object.keys(dict), newValences];
    }
  },

  mounted() {
    var ctx = document.getElementById(`chart-${this.playlistId}`);

    let dates = this.tracksInfo.map(x => x.added_at);
    let valences = this.tracksFeatures.map(x => x.valence);
    if (this.optionGroup) {
      let grouped = this.group(this.optionGroup, dates, valences);
      dates = grouped[0];
      valences = grouped[1];
    } else {
      dates = dates.map(x => moment(x).format("Do MMM YYYY"));
    }

    var data = {
      labels: dates,
      datasets: [
        {
          label: "happiness",
          data: valences
        }
      ]
    };

    var options = {
      scales: {
        xAxes: [
          {
            /* type: "time", */
            distribution: "series"
            /* time: {
              unit: "day"
            } */
          }
        ],
        yAxes: [
          {
            ticks: {
              suggestedMin: 0,
              suggestedMax: 1
            }
          }
        ]
      }
    };

    var myChart = new Chart(ctx, {
      type: "line",
      data: data,
      options: options
    });
  }
};
</script>
<template>
  <div>
    <canvas :id="'chart-' + playlistId" width="400" height="400"></canvas>
  </div>
</template>

<style>
</style>

<script>
import Chart from "chart.js";
import moment from "moment";

export default {
  props: ["playlistId", "tracksInfo", "tracksFeatures"],

  mounted() {
    var ctx = document.getElementById(`chart-${this.playlistId}`);

    console.log(moment("2016-10-11T13:44:40Z").format("DD MMMM YYYY"));

    var data = {
      labels: this.tracksInfo.map(x => x.added_at),
      datasets: [
        {
          data: this.tracksFeatures.map(
            x =>
              /* moment(x.valence).format("DD MMMM YYYY") */
              x.valence
          )
        }
      ]
    };

    var options = {
      scales: {
        xAxes: [
          {
            type: "time",
            distribution: "series",
            time: {
              unit: "day"
            }
          }
        ]
      }
    };

    var myChart = new Chart(ctx, {
      type: "line",
      data: data
    });
  }
};
</script>
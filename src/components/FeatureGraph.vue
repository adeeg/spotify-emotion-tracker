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
          return moment(date).format("Do MMM YYYY hh:mm:s");
      }
      return moment(date).format("Do MMM YYYY hh:mm:s");
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
    },

    newGroup: function(groupMethod, tracksInfos, tracksFeatures) {
      let dict = {};

      let dates = tracksInfos.map(x => x.added_at);

      // group together into dict
      for (let i = 0; i < dates.length; i++) {
        let date = dates[i];
        let trackInfo = tracksInfos[i];
        let trackFeatures = tracksFeatures[i];

        let combTrackData = Object.assign({}, trackInfo, trackFeatures);

        let key = this.getGroupFormat(groupMethod, date);

        if (key in dict) {
          dict[key].push(combTrackData);
        } else {
          dict[key] = [combTrackData];
        }
      }

      return [Object.keys(dict), Object.values(dict)]
    },

    getLineBackground: function(chart, valences) {
      const GREEN = "rgba(6, 214, 160, 0.5)";
      const RED = "rgba(239, 71, 111, 0.5)";
      const BLUE = "rgba(38, 84, 124, 0.5)";
      const WHITE = "rgba(252, 252, 252, 0.5)";
      const YELLOW = "rgba(255, 209, 102, 0.5)";

      //var width = window.innerWidth || document.body.clientWidth;
      var gradient = chart
        .getContext("2d")
        .createLinearGradient(0, 0, chart.width, 0);
      /* gradient.addColorStop(0, GREEN);
      gradient.addColorStop(1, RED); */
      let valCols = valences.map(x => {
        if (x > 0.6) {
          return GREEN;
        } else if (x > 0.4) {
          return WHITE;
        } else {
          return RED;
        }
      });

      for (let i = 0; i < valCols.length; i++) {
        var perct = i / valCols.length;
        gradient.addColorStop(perct, valCols[i]);
      }

      return gradient;
    }
  },

  mounted() {
    var chart = document.getElementById(`chart-${this.playlistId}`);

    let dates = this.tracksInfo.map(x => x.added_at);
    let combTrackData = [];

    for (let i = 0; i < dates.length; i++) {
      let trackInfo = this.tracksInfo[i];
      let trackFeatures = this.tracksFeatures[i]; 

      let combTrackD = Object.assign({}, trackInfo, trackFeatures);
      combTrackData.push(combTrackD);
    }
    combTrackData = combTrackData.map(x => [x]);
    let valences = this.tracksFeatures.map(x => x.valence);


    if (this.optionGroup) {
      let grouped = this.newGroup(this.optionGroup, this.tracksInfo, this.tracksFeatures);
      dates = grouped[0];
      combTrackData = grouped[1];

      // reduce valences (avg)
      let valences = [];
      for (const vals of combTrackData) {
        let vv = vals.map(x => x.valence);
        let mean = vv.reduce((a, b) => a + b, 0) / vv.length;
        valences.push(mean);
      }
    }

    var data = {
      labels: dates,
      datasets: [
        {
          label: "Happiness",
          data: valences,
          metadata: combTrackData
        }
      ]
    };

    var options = {
      layout: {
        padding: {
          left: 0,
          right: 0
        }
      },
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
      },
      tooltips: {
        callbacks: {
          //title: (tooltip, data) => "dog title",
          //label: (items, data) => items.metadata,
          afterLabel: function(tooltip, data) {
            let metadata = data['datasets'][0]['metadata'][tooltip['index']];

            let strings = metadata.map(x => '- ' + x['track']['artists'][0]['name']
                         + ' - '
                         + x['track']['name']
                         + ': '
                         + x['valence']);
            strings.unshift("");

            return strings;
          }
        },
        titleFontSize: 16,
        displayColors: false
      }
    };

    // thanks to https://github.com/chartjs/Chart.js/issues/3071#issuecomment-371001496
    var plugins = [
      {
        beforeRender: function(c, options) {
          var dataset = c.data.datasets[0];
          var yScale = c.scales["y-axis-0"];
          var yPos = yScale.getPixelForValue(0);

          /* var yScale = c.scales["y-axis-0"];
          var yPos = yScale.getPixelForValue */ 0;

          //let gradient = this.getLineBackground(chart, valences);
          // get gradient
          const GREEN = "rgba(6, 214, 160, 0.5)";
          const RED = "rgba(239, 71, 111, 0.5)";
          const BLUE = "rgba(38, 84, 124, 0.5)";
          const WHITE = "rgba(252, 252, 252, 0.5)";
          const YELLOW = "rgba(255, 209, 102, 0.5)";

          var vertGradient = c.ctx.createLinearGradient(0, 0, 0, c.height);

          vertGradient.addColorStop(0, GREEN);
          vertGradient.addColorStop(
            yScale.getPixelForValue(0.6) / c.height,
            WHITE
          );
          vertGradient.addColorStop(
            yScale.getPixelForValue(0.4) / c.height,
            WHITE
          );
          vertGradient.addColorStop(1, RED);

          /* var gradient = c.ctx.createLinearGradient(0, 0, c.width, 0); */

          /* options.scales.xAxes[0].ticks.stepSize; */

          /* let valCols = valences.map(x => {
            if (x > 0.6) {
              return GREEN;
            } else if (x > 0.4) {
              return WHITE;
            } else {
              return RED;
            }
          });
          for (let i = 0; i < valences.length; i++) {
            var perct = i / valCols.length;
            let end = perct + 0.05;
            let start = perct - 0.05;
            if (start >= 0) gradient.addColorStop(start, GREEN);
            if (end <= 1) gradient.addColorStop(end, RED);
          } */

          /* let colForValence = x => {
            if (x > 0.6) {
              return GREEN;
            } else if (x > 0.4) {
              return WHITE;
            } else {
              return RED;
            }
          }; */

          /* gradient.addColorStop(0, GREEN);
      gradient.addColorStop(1, RED); */
          /* let valCols = valences.map(x => {
            if (x > 0.6) {
              return GREEN;
            } else if (x > 0.4) {
              return WHITE;
            } else {
              return RED;
            }
          });
          for (let i = 0; i < valences.length; i++) {
            var perct = i / valCols.length;
            gradient.addColorStop(perct, valCols[i]);
            if (i !== 0) gradient.addColorStop(perct - 0.01, valCols[i]);
            if (i !== valences.length - 1)
              gradient.addColorStop(perct + 0.01, valCols[i]);
          } */

          /* let prev;
          for (let i = 0; i < valences.length; i++) {
            let col = colForValence(valences[i]);

            if (i == 0) prev = valence;
            if (i == valences.length - 1) prev = valence;

            // add the gradient stop for the previous section
            if (valence !== prev) {
            }
          } */

          /* for (let i = 0; i < valCols.length; i++) {
            var perct = i / valCols.length;
            gradient.addColorStop(perct, valCols[i]);
          } */

          var model =
            c.data.datasets[0]._meta[Object.keys(dataset._meta)[0]].dataset
              ._model;
          model.backgroundColor = vertGradient;
        }
      }
    ];

    var myChart = new Chart(chart, {
      type: "line",
      data: data,
      options: options,
      plugins: plugins
    });
  }
};
</script>
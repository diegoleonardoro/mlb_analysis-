var defaultURL = "/mendoza_averages";

function buildPlot() {
  d3.json(defaultURL).then(function (response) {
    console.log(response);
    var data = [response];
    var layout = { margin: { t: 30, b: 100 } };
    Plotly.plot("mendoza_averages", data, layout)

  }

  )
};

buildPlot()
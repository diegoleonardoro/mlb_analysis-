
var url ="/total_averages";

function buildPlot(){
d3.json(url).then(function (response){
    console.log(response);
    
    
    }


};
    
    
    
    
    
 var url = "/data";

function buildPlot() {
  d3.json(url).then(function(response) {

    console.log(response);
    var trace = {
      type: "scatter",
      mode: "lines",
      name: "Bigfoot Sightings",
      x: response.map(data => data.year),
      y: response.map(data => data.sightings),
      line: {
        color: "#17BECF"
      }
    };
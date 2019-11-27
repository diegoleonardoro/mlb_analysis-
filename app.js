
var url ="/mendoza_averages";

function buildPlot(){
  d3.json(url).then(function (response){
      console.log(response);
    
    
    var array_lenght = response.length;
    function range(start, end) {
      var ans = [ ];
      for (let i = start; i <= end; i++) {
          ans.push(i);
      }
      return ans;
     }
  
      var trace1 =  {
        x: [range( 0, array_lenght)],
        y: [response.mendonza_average],
        mode: 'lines',
        name: 'Lines'
      };
      
      var trace2 = {
           x: [range( 0, array_lenght)],
           y: [response.mendonza_average],
           mode: 'lines',
           name: 'Lines',
      };
      
      var data = [trace1, trace2]
      
      Plotly.newPlot('mendo_plot',data);
      }
  )};
  
    
    
    

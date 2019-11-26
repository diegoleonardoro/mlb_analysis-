
var url ="/total_averages";



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

    var trace =  {
        x: [range( 0, array_lenght  )],
      y: [response],
      mode: 'lines',
      name: 'Lines'
} 
    }
)};

    
    
    
    
    

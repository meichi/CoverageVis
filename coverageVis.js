var margin = {top: 20, bottom: 20, left: 30, right: 30},                    
    width = 1024 - margin.left - margin.right,                              
    height = 1080 - margin.top - margin.bottom;                             
                                                                                 
var xScale = d3.scale.linear().range([0, width]);                                
var yScale = d3.scale.linear().range([height, 0]);                               
                                                                            
var colorScale = d3.interpolateLab("#008000", "#c83a22");                        
var importanceScale = d3.scale.linear().range([0, 0.99]);                   
                                                                               
var radiusScale = d3.scale.linear();                                             
radiusScale.range([10, 50]);                                                     
                                                                                 
var xAxis = d3.svg.axis()                                                   
    .scale(x)                                                               
    .orient("bottom");                                                      
                                                                             
var yAxis = d3.svg.axis()                                                   
    .scale(y)                                                               
    .orient("left");          


var redraw = function(dataset){
    console.log(i);
};



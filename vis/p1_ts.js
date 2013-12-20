/**
 * Timeseries plot of top-five contractors for 2001 - 2003
 */

// set margin and init svg in the body
var margin = {top: 100, right: 120, bottom: 200, left: 220},
    width = 700 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

var svg = d3.select("body").append("svg")
                .attr( { "width": width + margin.left + margin.right,
                         "height": height + margin.top + margin.bottom
                })
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// establish/set y axis scale and range
var y = d3.scale.linear()
            .range([height, 0]);

var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

// establish/set time axis scale and range
var t = d3.time.scale()
            .range([0, width]);

var tAxis = d3.svg.axis()
            .scale(t)
            .orient("bottom");

// set up colors, areas, and the stack layout
var color = d3.scale.category20();

var area = d3.svg.area()
            .x(function(d) { return t(d.date); })
            .y0(function(d) { return y(d.y0); } )
            .y1(function(d) { return y(d.y0 + d.y); });

var stack = d3.layout.stack()
                .values( function(d) { return d.values; } );

// load data, insert into svg elements                    

            

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
d3.csv("data/p1_ts_data.csv", function( row ) {

/*
 * Using d3's built in area chart requres that the date be the primary key and
 * that, in this case, each company must have an equal number of dates.
 *
 * To do this, create a time range. Iterate over each company. If the company
 * has an entry for a date in the time range, add this to the previous total.
 * If not, make the next entry the previous total.
 */



});

            

/**
 * Example script for making the contractor bar chart. Use this as a reference
 * for now.
 */
var margin = {top: 100, right: 120, bottom: 200, left: 220},
    width = 700 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

var y = d3.scale.ordinal()
    .rangeRoundBands([0, height], 0.1);

var x = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(10);

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("p1_hist_data.csv", function(error, data) {

  y.domain(data.map(function(d) { return d.contractor; }));
  x.domain([d3.max(data, function(d) { return parseFloat(d.total); }), 0]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text");

  svg.append("text")
      .attr("class", "x label")
      //.style("stroke","red")
      .attr("x", width/2)
      .attr("y", height + margin.bottom*0.35)
      .text("Billions of US Dollars");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);
  svg.append("text")
      .attr("class", "y label")
      .attr("y", -margin.top*0.15)
      .attr("x", 0)
      .attr("text-anchor", "end")
      .text("Contractor");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("y", function(d) { return y(d.contractor); })
      .attr("height", y.rangeBand())
      .attr("x", 0)
      .attr("width", function(d) { return x(d.total); });
});

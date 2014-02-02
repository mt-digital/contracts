/**
 * Timeseries plot of top-five contractors for 2001 - 2003
 */

// set margin and init svg in the body
var margin = {top: 100, right: 210, bottom: 200, left: 220},
    width = 1100 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;

var svg = d3.select("body").append("svg")
                .attr( { "width": width + margin.left + margin.right,
                         "height": height + margin.top + margin.bottom
                })
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// append rectangle that spans plot area, taken from http://bl.ocks.org/mbostock/3892919
svg.append("rect")
    .attr("class", "background")
    .attr({"width":width, "height":height});

// establish/set y axis scale and range
var y = d3.scale.linear()
            .range([height, 0]);

var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            // extend white(-on-grey) ticks for width of plot space
            .tickSize(-width);

// establish/set time axis scale and range
var t = d3.time.scale()
            .range([0, width]);

var tAxis = d3.svg.axis()
            .scale(t)
            .orient("bottom");

// set up colors, areas, and the stack layout
var color = d3.scale.category20();

var area = d3.svg.area()
            .x(function(d) { return t(d.day); })
            .y0(function(d) { return y(d.y0); } )
            .y1(function(d) { return y(d.y0 + d.y); });

var stack = d3.layout.stack()
                .values( function(d) { return d.values; } );

// load data, insert into svg elements                    
d3.csv("data/p1_ts_data.csv", function(error, row ) {
/*
 * Using d3's built in area chart requres that the date be the primary key and
 * that, in this case, each company must have an equal number of dates.
 *
 * To do this, create a time range. Iterate over each company. If the company
 * has an entry for a date in the time range, add this to the previous total.
 * If not, make the next entry the previous total.
 */
    color.domain(d3.keys(row[0]).filter(function(key) { return key !== "day"; }
        )
    );

    row.forEach( function(d) {
        d.day = d3.time.format.iso.parse(new Date( parseInt(d.day)*1000 ) );
    });

    // create named series of each contractor's timeseries 
    var contractors = stack( color.domain().map( function(c) {
        return {
        	name: c,
        	values: row.map( function(d) {
        		return { day: d.day, y: parseFloat(d[c]) };
        	})
        };
    }));

    t.domain(d3.extent( contractors[0].values, function(d){ return d.day; } ));
    //tAxis.ticks(7);
    tAxis.ticks(d3.time.month, 6);
    tAxis.tickFormat(d3.time.format("%Y-%m"));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(tAxis);

    y.domain( [0, 225000000000] );
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    var contractor = svg.selectAll(".contractor")
            .data(contractors)
        .enter().append("g")
            .attr("class", "contractor");

    contractor.append("path")
        .attr("class", "area")
        .attr("d", function(d) { return area( d.values ); })
        .style("fill", function(d) { return color( d.name ); });

    
    var legendFontSize = 14; 
    // make legend
    svg.append("rect")
        .attr("class", "background")
        .attr("x", width + 0.1*margin.right)
        .attr("y", 0)
        .attr("width", margin.right*0.9)
        .attr("height", contractors.length*(legendFontSize+2)+7);
    
    svg.selectAll(".legend text")
        .data(color.domain())
        .enter()
        .append("text")
        .attr("class","legend text")
        .attr("text-anchor","end")
        .attr("fill", "black")
        .attr("font-size", legendFontSize.toString())
        .attr("x", width + 0.75*margin.right)
        .attr("y", function(d, i) { return (1 + i)*(legendFontSize + 2); })
        .text( function(d) { return d; } );

    svg.selectAll(".legend element")
        .data(color.range().slice(0,color.domain().length))
        .enter()
        .append("rect")
        .attr("class","legend element")
        .attr("x", width + 0.8*margin.right)
        .attr("y", function(d,i) { return i*legendFontSize + 2; })
        .attr("height", legendFontSize - 2)
        .attr("width", 0.175*margin.right)
        .attr("fill", function(d){ return d; });
});

/**
 * Make a legend where each contractor shows its unique color
 */
            

var zonesData = window.zones_json;
var margin = {top: 10, right: 10, bottom:40, left:40};
var dimension = {maxWidth: 800, HtoWRatio: 0.6};
var zoneNames = [
                    'Zone 1 (20\')',
                    'Zone 2 (40\')',
                    'Zone 3 (60\')',
                    'Zone 4 (80\')',
                    'Zone 5 (100\')'
                ];
var transectNames = ['Conifers', 'Hardwoods', 'Shrubs'];

var createGraph = function createGraph() {
    // Set up width and height for the container div#rip-graph and actual graph
    var containerWidth = Math.min($('div#rip-graph').parent().width(), dimension.maxWidth);
    var containerHeight = containerWidth * dimension.HtoWRatio;
    var graphWidth = containerWidth - margin.left - margin.right;
    var graphHeight = containerHeight - margin.top - margin.bottom;

    $('div#rip-graph').width(containerWidth).height(containerHeight);

    var svg = d3.select('div#rip-graph').append('svg')
              .attr('width', "100%")
              .attr('height', "100%");

    var g = svg.append('g')
            .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    var xBackground = d3.scaleLinear()
                      .domain([0, 1])
                      .range([0, graphWidth]);
    var x = d3.scaleOrdinal()
            .domain(zoneNames)
            .range([50,150,250,350,450]);

    var y = d3.scaleLinear()
            .domain([0, getXMax()])
            .range([graphHeight, 0]);

    var xBackgroundAxis = d3.axisBottom(xBackground)
                          .tickFormat("")
                          .ticks(6);
    var xAxis = d3.axisBottom(x)
                .ticks(6)
                .tickSize(0);
    var yAxis = d3.axisLeft(y)
                .tickSize(10);
    svg.append('g')
       .call(yAxis)
       .attr('transform', 'translate(' + margin.left + ', ' + 0 + ')');
    svg.append('g')
       .call(xAxis);
    svg.append('g')
       .call(xBackgroundAxis);
}

var getXMax = function getXMax() {
    // Get the max number of zones data to set up y axis range
    var max = 0;
    zonesData.forEach(function(zone) {
        var zoneArr = [zone.conifers, zone.hardwoods, zone.shrubs];
        var zoneMax = Math.max.apply(null, zoneArr);
        max = Math.max(max, zoneMax);
    });
    return Math.ceil(max / 10) + max;
}

var clearGraph = function clearGraph() {
    $('div#rip-graph svg').remove();
}

$(function() {
    // Create graph on page load
    createGraph();
});

$(window).resize(function() {
    // Recreate graph (redraw) on resize window
    clearGraph();
    createGraph();
});

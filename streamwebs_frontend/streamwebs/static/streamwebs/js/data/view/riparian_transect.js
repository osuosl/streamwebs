var zonesData = window.zones_json;
var margin = {top: 10, right: 16, bottom:10, left:28};
var dimension = {maxWidth: 800, HtoWRatio: 0.6, graphZoneMargin: 3};
var zoneNames = [
    'Zone 1',
    'Zone 2',
    'Zone 3',
    'Zone 4',
    'Zone 5'
];
var distances = [
    '(0\')',
    '(20\')',
    '(40\')',
    '(60\')',
    '(80\')',
    '(100\')'
]
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

    var graph = svg.append('g')
                   .attr('transform', 'translate(' + 0 + ', ' + 0 + ')');

    createAxis(graph, graphWidth, graphHeight);
    createBars(graph, graphWidth, graphHeight)
}

var createAxis = function createAxis(graphContainer, graphWidth, graphHeight) {
    var xBackground = d3.scaleLinear()
                        .domain([0, 1])
                        .range([0, graphWidth]);

    var xBackground = d3.scaleOrdinal()
                        .domain(distances)
                        .range(getDistanceRange(graphWidth));

    var x = d3.scaleOrdinal()
              .domain(zoneNames)
              .range(getZoneRange(graphWidth));

    var y = d3.scaleLinear()
              .domain([0, getXMax()])
              .range([graphHeight, 0]);

    var xBackgroundAxis = d3.axisBottom(xBackground)
                            .ticks(6);

    var xAxis = d3.axisBottom(x)
                  .tickSize(0);

    var yAxis = d3.axisLeft(y);

    graphContainer.append('g')
                  .call(xBackgroundAxis)
                  .attr('transform', 'translate(' + margin.left + ', ' + graphHeight + ')');

    graphContainer.append('g')
                  .call(xAxis)
                  .attr('transform', 'translate(' + margin.left + ', ' + graphHeight + ')');

    graphContainer.append('g')
                  .call(yAxis)
                  .attr('transform', 'translate(' + margin.left + ', ' + 0 + ')');
}

var getDistanceRange = function getDistanceRange(graphWidth) {
    var rangeArr = [];
    var rangeWidth = graphWidth / 5;
    for (var i = 0; i < 6; i++) {
        rangeArr.push(i * rangeWidth);
    }
    return rangeArr;
}

var getZoneRange = function getZoneRange(graphWidth) {
    var rangeArr = [];
    var rangeWidth = graphWidth / 5;
    for (var i = 0; i < 5; i++) {
        rangeArr.push((i + 0.5) * rangeWidth);
    }
    return rangeArr;
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

var createBars = function createBars(graphContainer, graphWidth, graphHeight) {
    graphContainer.append('g').selectAll('g')
        .data(zonesData)
        .enter().append('g')
            .attr('transform', function(d, i) {

            })

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

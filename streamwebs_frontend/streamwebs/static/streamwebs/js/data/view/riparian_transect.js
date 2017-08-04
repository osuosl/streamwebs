// Data related variables
var zonesData = window.zones_json;
var dataKeys = ['conifers', 'hardwoods', 'shrubs'];

// Properties of the graph
var barColor = ['#F73A23','#A14728', '#65B239'];
var margin = {top: 16, right: 16, bottom:30, left:28};
var dimension = {
    maxWidth: 800,
    HtoWRatio: 0.6,
    graphZoneMargin: 6,
    graphBarMargin: 2,
    xAxisHeight: 10, // Change depend on xAxis label font size

    legendBoxHeight: 72,
    legendLeftMargin: 40,
    marginBetweenLegend: 6,
};



// Strings for each zones and ticks
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

var createGraph = function createGraph() {
    // Set up width and height for the container div#rip-graph and actual graph
    var containerWidth = Math.min($('div#rip-graph').parent().width(), dimension.maxWidth);
    var containerHeight = containerWidth * dimension.HtoWRatio + dimension.legendBoxHeight;
    var graphWidth = containerWidth - margin.left - margin.right;
    var graphHeight = containerHeight - margin.top - margin.bottom - dimension.legendBoxHeight;
    $('div#rip-graph').width(containerWidth).height(containerHeight);

    var svg = d3.select('div#rip-graph').append('svg')
                .attr('width', '100%')
                .attr('height', '100%');

    var graph = svg.append('g')
                    .attr('transform', 'translate(' + 0 + ', ' + 0 + ')');

    var legendsContainer = svg.append('g')
                        .attr('transform', 'translate(' + dimension.legendLeftMargin
                            + ', ' + (containerHeight - dimension.legendBoxHeight)
                            + ')'
                        );

    // Set up the scales for the axis
    var xBackground = d3.scaleOrdinal()
                        .domain(distances)
                        .range(getDistanceRange(graphWidth));

    var x = d3.scaleOrdinal()
                .domain(zoneNames)
                .range(getZoneRange(graphWidth));

    var y = d3.scaleLinear()
                .domain([0, getXMax()])
                .range([graphHeight - dimension.xAxisHeight, 0]);

    createAxis(graph, graphWidth, graphHeight, xBackground, x, y);
    createBars(graph, graphWidth, graphHeight, y);
    createLegends(legendsContainer);
}

var createAxis = function createAxis(graphContainer, graphWidth, graphHeight, xBackground, x, y) {

    // Take in the x and y scales to create axis, and append them to containers
    var xBackgroundAxis = d3.axisBottom(xBackground)
                            .ticks(6);

    var xAxis = d3.axisBottom(x)
                    .tickSize(0);

    var yAxis = d3.axisLeft(y);

    graphContainer.append('g')
                    .call(xBackgroundAxis)
                    .attr('transform', 'translate(' + margin.left + ', '
                        + (graphHeight + margin.top - dimension.xAxisHeight) + ')'
                    );

    graphContainer.append('g')
                    .call(xAxis)
                    .attr('transform', 'translate(' + margin.left + ', '
                        + (graphHeight + margin.top - dimension.xAxisHeight) + ')'
                    );

    graphContainer.append('g')
                    .call(yAxis)
                    .attr('transform', 'translate(' + margin.left + ', '
                        + margin.top + ')'
                    );
}

var getDistanceRange = function getDistanceRange(graphWidth) {
    // Output the array of coordinates for ticks for distances
    var rangeArr = [];
    var rangeWidth = graphWidth / 5;
    for (var i = 0; i < 6; i++) {
        rangeArr.push(i * rangeWidth);
    }
    return rangeArr;
}

var getZoneRange = function getZoneRange(graphWidth) {
    // Output the array of coordinates for ticks for zones
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

var createBars = function createBars(graphContainer, graphWidth, graphHeight, yScale) {
    var groupWidth = graphWidth / 5;
    var barWidth = (groupWidth - 2 * dimension.graphZoneMargin - 4 * dimension.graphBarMargin) / 3;
    var groups = graphContainer.append('g').selectAll('g')
        .data(zonesData)
        .enter().append('g')
            .attr('transform', function(d, i) {
                return ('translate('
                    + (i * groupWidth + dimension.graphZoneMargin + margin.left)
                    + ', ' + margin.top + ')'
                );
            })
        .selectAll('rect')
        .data(function(d) {
            return dataKeys.map(function(key) {
                return {key: key, value: d[key]}
            });
        })
        .enter().append('rect')
            .attr('width', barWidth)
            .attr('height', function(d, i) {
                return (graphHeight - yScale(d.value) - dimension.xAxisHeight);
            })
            .attr('fill', function(d, i) { return barColor[i]; })
            .attr('x', function(d, i) {
                return i * barWidth + (i + 1) * dimension.graphBarMargin;
            })
            .attr('y', function(d, i) { return yScale(d.value); });
}

var createLegends = function createlegends(legendsContainer) {
    var legendHeight = (dimension.legendBoxHeight - 2 * dimension.marginBetweenLegend) / 3;
    var font_size = 14;

    dataKeys.forEach(function(d, i) {
        var legend = legendsContainer.append('g')
            .attr('transform', 'translate(' + 0 + ', '
                + (i * (dimension.marginBetweenLegend + legendHeight)) + ')');
        legend.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', legendHeight)
            .attr('height', legendHeight)
            .attr('fill', barColor[i]);

        legend.append('text')
            .attr('x', 24)
            .attr('y', font_size)
            .attr('font-size', font_size + 'px')
            .text(d);
    });
}

var clearGraph = function clearGraph() {
    $('div#rip-graph svg').remove();
}

/***********************************************************************
*               Initializing & window related
***********************************************************************/

$(function() {
    // Create graph on page load
    createGraph();
});

$(window).resize(function() {
    // Recreate graph (redraw) on resize window
    clearGraph();
    createGraph();
});

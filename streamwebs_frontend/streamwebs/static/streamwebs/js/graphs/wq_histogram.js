"use strict";

function toFixed(value, precision) {
    var power = Math.pow(10, precision || 0);
    return String(Math.round(value * power) / power);
}

var createGraph = function createGraph() {
    $('svg').remove();

    var data = JSON.parse(JSON.stringify(window.data));

    var formatted = data.map(function (d) {
        return d.samples.reduce(function (prev, curr, idx) {
            /*
             * This is more straightforward than it looks. Prev is the average
             * of samples[0] through samples[idx-1]. We multiply it by the
             * of points we've calculated so far (since idx is 0-indexed, it's
             * just that), which is the total. Add the new value, then divide
             * again.
             *
             * Thus we can calculate an average on the fly without explicitly
             * summing and dividing.
             */
            return ((prev * idx) + parseFloat(curr[key])) / (idx + 1);
        }, 0);
    });

    var margin = {top: 50, right: 20, bottom: 20, left: 50};

    var containerName = '#histogram';
    var container = $(containerName);
    var width = container.width() - margin.left - margin.right;
    var height = (container.width() * 0.6) - margin.top - margin.bottom;

    var svg = d3.select(containerName).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var range = d3.extent(formatted);

    if (range[0] === range[1]) {
        range[0]--;
        range[1]++;
    }

    var x = d3.scaleLinear()
        .domain(range)
        .range([0, width])
        .nice();

    var bins = d3.histogram()
        .domain(x.domain())
        .thresholds(20)
        (formatted);

    var y = d3.scaleLinear()
        .range([height, 0])
        .domain(d3.extent(bins, function (d) {
             return d.length;
         })
        )
        .nice();

    var xAxis = d3.axisBottom(x);
    xAxis.ticks(0);

    var yAxis = d3.axisLeft(y);
    var yMax = y.domain()[1];
    /*
     * Array(n) creates an array of n values. Array.keys() returns an array
     * iterator which returns the keys of the array (i.e. the numbers 0-n);
     * the spread operator [... ] unpacks something like an iterator into
     * an array. In short, this line is the Javascript equivalent of Python's
     * range() function.
     */
    yAxis.tickValues([...Array(yMax+1).keys()]);

    svg.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

    svg.append('g')
        .attr('class', 'axis axis--y')
        .call(yAxis);

    var histogram = svg.selectAll('.bar')
        .data(bins)
        .enter().append('g')
            .attr('class', 'bar')
            .attr('transform', function (d) {
                'translate(' + x(d.x0) + ',' + y(d.length) + ')';
            });

    histogram.append('rect')
        .attr('x', 1)
        .attr('width', function (d) {
            x(d.x1) - x(d.x0) - 1;
        })
        .attr('height', function (d) {
            height - y(d.length)
        });

    histogram.append('text')
        .attr('class', 'label')
        .attr('dy', '.75em')
        .attr('x', function (d) {
            (x(d.x1) - x(d.x0))/2;
        })
        .attr('y', 6)
        .attr('text-anchor', 'middle')
        .text(function (d) {
            d.length ? d3.format(',.0f')(d.length) : '';
        });

    histogram.append('text')
        .attr('class', 'value')
        .attr('dy', '.75em')
        .attr('x', function (d) {
            (x(d.x1) - x(d.x0))/;
        })
        .attr('y', function (d) {
            height - y(d.length) + 6;
        })
        .attr('text-anchor', 'middle')
        .text(function (d) {
            toFixed(Number.parseFloat(d.x0), 2);
        });
};

$(function () {
    createGraph();
});

$(window).resize(function () {
    createGraph();
});

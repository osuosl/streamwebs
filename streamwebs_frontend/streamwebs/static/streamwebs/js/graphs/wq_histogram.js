"use strict";

const createGraph = function createGraph() {
    $('svg').remove();

    let data = JSON.parse(JSON.stringify(window.data));

    const formatted = data.map(d => {
        return d.samples.reduce((prev, curr, idx) => {
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

    const margin = {top: 50, right: 20, bottom: 20, left: 50};

    const containerName = '#histogram';
    const container = $(containerName);
    const width = container.width() - margin.left - margin.right;
    const height = (container.width() * 0.6) - margin.top - margin.bottom;

    const svg = d3.select(containerName).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    const range = d3.extent(formatted);

    if (range[0] === range[1]) {
        range[0]--;
        range[1]++;
    }

    const x = d3.scaleLinear()
        .domain(range)
        .range([0, width]);

    const bins = d3.histogram()
        .domain(x.domain())
        .thresholds(20)
        (formatted);

    const y = d3.scaleLinear()
        .range([height, 0])
        .domain(d3.extent(bins, d => d.length));

    const xAxis = d3.axisBottom(x);
    xAxis.ticks(0);

    const yAxis = d3.axisLeft(y);
    const yMax = y.domain()[1];
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

    const histogram = svg.selectAll('.bar')
        .data(bins)
        .enter().append('g')
            .attr('class', 'bar')
            .attr('transform', d => 'translate(' + x(d.x0) + ',' + y(d.length) + ')');

    histogram.append('rect')
        .attr('x', 1)
        .attr('width', d => x(d.x1) - x(d.x0) - 1)
        .attr('height', d => height - y(d.length));

    histogram.append('text')
        .attr('class', 'label')
        .attr('dy', '.75em')
        .attr('x', d => (x(d.x1) - x(d.x0))/2)
        .attr('y', 6)
        .attr('text-anchor', 'middle')
        .text(d => d.length ? d3.format(',.0f')(d.length) : '');

    histogram.append('text')
        .attr('class', 'value')
        .attr('dy', '.75em')
        .attr('x', d => (x(d.x1) - x(d.x0))/2)
        .attr('y', d => height - y(d.length) + 6)
        .attr('text-anchor', 'middle')
        .text(d => d.x0);
};

$(() => {
    createGraph();
});

$(window).resize(() => {
    createGraph();
});

let data = JSON.parse(JSON.stringify(window.data));

let date_range = [0, Number.MAX_SAFE_INTEGER];

const changeRangeStart = function changeRangeStart() {
    if (!$(this).val()) { // If the field is empty, clear the range
        date_range[0] = 0;
    } else {
        const date = Date.parse($(this).val());
        if (!date || Number.isNaN(date)) {
            return;
        }

        date_range[0] = date;
    }

    createGraph();
};

const changeRangeEnd = function changeRangeEnd() {
    if (!$(this).val()) { // If the field is empty, clear the range
        date_range[1] = Number.MAX_SAFE_INTEGER;
    } else {
        const date = Date.parse($(this).val());
        if (!date || Number.isNaN(date)) {
            return;
        }

        date_range[1] = date;
    }

    createGraph();
};

const createGraph = function createGraph() {
    const outerContainer = $('#graph-' + siteId + '-container');
    outerContainer.find('svg').remove();

    data = JSON.parse(JSON.stringify(window.data)); // Copy the data so we don't change the original

    const formatted = [];

    for (let key in data) {
        const date = parseInt(key, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        formatted.push(data[key]);
    }

    formatted.sort((a, b) => {
        return a.date - b.date;
    });
    
    /***************************************************************************
     * Temperature
     **************************************************************************/

    const container = outerContainer.find('graph-' + siteId + '-temperature');
    const margin = {top: 20, right: 150, bottom: 30, left: 40};
    const width = (container.width() * 0.5) - margin.left - margin.right;
    const height = 192 - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .domain(d3.extent(formatted, (d) => { return d.date }))
        .range([0, width]);
    const y = d3.scaleLinear()
        .domain([0,
            d3.max(formatted, (d) => {
                return Math.max(d.water_temperature, d.air_temperature);
            })
        ])
        .range([height, 0]);
    const z = d3.scaleOrdinal()
        .domain(types.map((c) => { return c.name }))
        .range(['#869099', '#8c7853', '#007d4a', '#e24431']);

    const line = d3.line()
        .curve(d3.curveBasis)
        .x((d) => { return x(d.date) })
        .y((d) => { return y(d.value) });

    const svg = d3.select('#graph-' + siteId).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    const g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    g.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(d3.axisBottom(x));

    g.append('g')
        .attr('class', 'axis axis--y')
        .call(d3.axisLeft(y));

    const type = g.selectAll('.type')
        .data(types)
        .enter()
    .append('g')
        .attr('class', 'type');

    type.append('path')
        .attr('class', 'line')
        .attr('d', (d) => { return line(d.values) })
        .style('stroke', (d) => { return z(d.name) });

    type.append('text')
        .datum((d) => {
            return {name: d.name, value: d.values[d.values.length - 1]}
        })
        .attr('transform', (d) => {
            return 'translate(' + x(d.value.date) + ',' + y(d.value.value) + ')';
        })
        .attr('x', 3)
        .attr('dy', '0.35em')
        .style('font', '10px sans-serif')
        .text((d) => { return d.name });
};

$(() => {
    $('input[type=date]').val('');
    $('#date-start').change(changeRangeStart);
    $('#date-end').change(changeRangeEnd);

    //createGraph();
});
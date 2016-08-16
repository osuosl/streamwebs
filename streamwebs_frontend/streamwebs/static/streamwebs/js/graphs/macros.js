let data = window.data_summ;

let date_range = [0, Number.MAX_SAFE_INTEGER];

const changeRangeStart = function changeRangeStart(e) {
    date_range[0] = e.data;
    data = data.filter((elem) => {
        return elem.date_time >= e.data; //TODO: Adjust for actual types
    });
};

const changeRangeEnd = function changeRangeEnd(e) {
    date_range[1] = e.data;
    data = data.filter((elem) => {
        return elem.date_time <= e.data; //TODO: Adjust for actual types
    });
};

const useLineGraph = function useLineGraph() {
    const outerContainer = $('#graph-' + siteId);
    outerContainer.find('div svg').remove();
    $('.graph-header').show();
    outerContainer.find('.graph-header').hide();

    data = JSON.parse(JSON.stringify(window.data_time)); // Copy the data so we don't change the original

    const formatted = [];

    for (let key in data) {
        const date = parseInt(key, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        let total = 0;
        for (let category in data[key]) {
            if (category === 'Sensitive') {
                data[key][category] /= 3;
            } else if (category === 'Somewhat Sensitive') {
                data[key][category] /= 2;
            }
            total += data[key][category];
        }
        data[key].date = new Date(date);
        data[key].Total = total;
        formatted.push(data[key]);
    }

    formatted.sort((a, b) => {
        return a.date - b.date;
    });

    formatted.columns = ['date', 'Tolerant', 'Somewhat Sensitive', 'Sensitive', 'Total'];

    const types = formatted.columns.slice(1).map((name) => {
        return {
            name: name,
            values: formatted.map((d) => {
                return {date: d.date, value: d[name]};
            })
        };
    });

    const container = outerContainer;
    const margin = {top: 20, right: 150, bottom: 30, left: 40};
    const width = (container.width() * 0.5) - margin.left - margin.right;
    const height = 192 - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .domain(d3.extent(formatted, (d) => { return d.date }))
        .range([0, width]);
    const y = d3.scaleLinear()
        .domain([0,
            d3.max(types, (c) => {
                return d3.max(c.values, (d) => { return d.value })
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

const useBarGraph = function useBarGraph() {
    const outerContainer = $('#graph-' + siteId);
    outerContainer.find('svg').remove();
    $('.graph-header').hide();
    outerContainer.find('.graph-header').show();

    data = JSON.parse(JSON.stringify(window.data_summ)); // Copy the data so we don't change the original

    const categories = {'tolerant': [], 'somewhat': [], 'sensitive': [], 'total': []};

    let numEntries = 0;
    for (let date in data) {
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        for (let category in data[date]) {
            let total = 0;
            for (let species of data[date][category]) { // Look at each animal
                let found = false;
                for (let entry of categories[category]) {
                    if (entry.name === species.name) { // If we've seen the animal
                        entry.value += species.value; // before, just sum it
                        found = true;
                        break;
                    }
                }

                if (!found) { // If we haven't seen this animal before, add it
                    categories[category].push(species);
                }
                total += species.value;
            }

            let found = false;
            for (let entry of categories['total']) {
                if (entry.name === category) {
                    entry.value += total;
                    found = true;
                    break;
                }
            }

            if (!found) {
                categories['total'].push({
                    name: category,
                    value: total,
                });
            }
        }
        numEntries++;
    }

    for (let category in categories) {
        for (let entry of categories[category]) {
            entry.value /= numEntries; // Earlier summed, now divide to get average
        }
    }

    for (let category in categories) {
        if (category == 'total') {
            continue;
        }

        const species = categories[category];

        const container = $('#graph-' + siteId + '-' + category);
        const margin = {top: 20, right: 20, bottom: 30, left: 40};
        const width = (container.width() * 0.5) - margin.left - margin.right;
        const height = 192 - margin.top - margin.bottom;

        const x = d3.scaleBand()
            .domain(species.map((d) => { return d.name }))
            .range([0, width])
            .paddingInner(0.1);
        const y = d3.scaleLinear()
            .domain([0, d3.max(species, (d) => { return d.value })])
            .range([height, 0]);

        const xAxis = d3.axisBottom(x);
        const yAxis = d3.axisLeft(y).ticks(10);

        const svg = d3.select('#graph-' + siteId + '-' + category).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis);

        svg.append('g')
            .attr('class', 'y axis')
            .call(yAxis)
        .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 6)
            .attr('dy', '.71em')
            .style('text-anchor', 'end')
            .text('Frequency');

        svg.selectAll('.bar')
            .data(species)
            .enter()
        .append('rect')
            .attr('class', 'bar')
            .attr('x', (d) => { return x(d.name) })
            .attr('width', x.bandwidth())
            .attr('y', (d) => { return y(d.value) })
            .attr('height', (d) => { return height - y(d.value) });
    }

    const totals = categories['total'];
    let sum = 0;
    for (let total of totals) {
        sum += total.value;
    }
    const names = {
        'sensitive': 'Sensitive',
        'somewhat': 'Somewhat Sensitive',
        'tolerant': 'Tolerant',
    };

    const container = $('#graph-' + siteId + '-pie');
    const width = container.width() * 0.5;
    const height = 256;
    const radius = Math.min(width, height) / 2;

    const color = d3.scaleOrdinal()
        .range(['#869099', '#8c7853', '#007d4a']);

    const arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    const labelArc = d3.arc()
        .outerRadius(radius - 40)
        .innerRadius(radius - 40);

    const pie = d3.pie()
        .sort(null)
        .value((d) => { return d.value });

    const svg = d3.select('#graph-' + siteId + '-pie').append('svg')
        .attr('width', width)
        .attr('height', height)
    .append('g')
        .attr('transform', 'translate(' + width/2 + ',' + height/2 + ')');

    const g = svg.selectAll('.arc')
        .data(pie(totals))
        .enter()
    .append('g')
        .attr('class', 'arc');

    g.append('path')
        .attr('d', arc)
        .style('fill', (d) => { return color(d.data.name) });

    g.append('text')
        .attr('transform', (d) => { return 'translate(' + labelArc.centroid(d) + ')' })
        .attr('dy', '.35em')
        .text((d) => {
            return names[d.data.name] + ' (' + ((d.value/sum)*100).toFixed(2) + '%)'
        });
};

// Fix for broken .change() event on radio buttons
// See: http://stackoverflow.com/questions/4028936/
$.fn.fix_radios = function fix_radios() {
    function focus() {
        if (!this.checked)
            return;
        if (!this.was_checked) {
            $(this).change();
        }
    }

    function change(e) {
        if (this.was_checked) {
            e.stopImmediatePropagation();
            return;
        }

        $('input[name=' + this.name + ']').each(function() {
            this.was_checked = this.checked;
        });
    }

    return this.focus(focus).change(change);
};

$(() => {
    $('#date-start').change(changeRangeStart);
    $('#date-end').change(changeRangeEnd);

    $('input[type=radio]').fix_radios();
    $('input[name=type]').change(() => {
        if ($('input[name=type]:checked').val() === 'line') {
            useLineGraph();
        } else {
            useBarGraph();
        }
    });

    $('#type-bar').change();
});
let data = window.data_summ;

let date_range = [0, Number.MAX_SAFE_INTEGER];

/*
 * Number.prototype.toFixed() has several problems: it doesn't
 * round consistently, and it always has the given precision, adding
 * zeroes to the end of the string if necessary. This will instead
 * provide a consistent rounding to the number of provided decimal places
 * OR the number of decimals in the number, whichever is lower:
 *
 * toFixed(Math.PI, 2) == "3.14"
 * toFixed(Math.PI, 3) == "3.142"
 * toFixed(10, 4) == "10"
 * toFixed(10.000000000001, 1) == "10"
 *
 * One unfortunate side note: scientific notation is maintained:
 *
 * toFixed(1e100, 2) == "1e+100"
 */
function toFixed(value, precision) {
    var power = Math.pow(10, precision || 0);
    return String(Math.round(value * power) / power);
}

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

    // Reload the graph with the new ranges.
    if ($('input[type=radio]:checked').val() == 'line') {
        useLineGraph();
    } else {
        useBarGraph();
    }
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

    // Reload the graph with the new ranges.
    if ($('input[type=radio]:checked').val() == 'line') {
        useLineGraph();
    } else {
        useBarGraph();
    }
};

const useLineGraph = function useLineGraph() {
    const outerContainer = $('#graph-' + siteId);
    outerContainer.find('svg').remove();
    $('.graph-header').show();
    outerContainer.find('.graph-header').hide();

    // Copy the data so we don't change the original
    data = JSON.parse(JSON.stringify(window.data_time));

    let formatted = [];

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

    /*
     * This section is a little confusing. What we want to do is take our data
     * and reduce it down to an average per day for which we have data.
     * So if we have 5 points on 2016-10-05, and 3 on 2016-10-19, we condense it
     * to one point for 2016-10-05 that's the average of those 5, and one points
     * for 2016-10-19 that's the average of those 3.
     *
     * So currently `formatted` looks like this:
     *
     * [
     *   {
     *     date: Date(...),
     *     Sensitive: ...,
     *     'Somewhat Sensitive': ...,
     *     Tolerant: ...,
     *     Total: ...,
     *   },
     *   {
     *     ...
     *   },
     *   ...
     * ]
     */
    formatted = formatted.map((x) => {
        /*
         * First we'll map the data to remove any extraneous values just in case,
         * and to change the date to a string of just the date.
         */
        const key = x.date.toISOString().substring(0, 10);

        return {
            date: key,
            Sensitive: x.Sensitive,
            'Somewhat Sensitive': x['Somewhat Sensitive'],
            Tolerant: x.Tolerant,
            Total: x.Total,
        };
    }).reduce((prev, curr) => {
        /*
         * Next, we'll reduce it down to sums per day.
         */

        /*
         * `data` here represents the existing data for the day we're looking at,
         * if it exists. It contains all of the sums we've already calculated for
         * this day, plus its own index in the list so we can find it later.
         */
        let data = prev.map((x, i) => {
            x['idx'] = i;
            return x;
        })
            .filter((x) => {
                return x.date === curr.date;
            });
        if (data === [] || data.length === 0) {
            /*
             * If this is the first data point we've found for this day, then we'll
             * add it as it is to the list. Also add a `count` value so we can
             * calculate the average from the sums.
             */
            prev.push({
                date: curr.date,
                Sensitive: curr.Sensitive,
                'Somewhat Sensitive': curr['Somewhat Sensitive'],
                Tolerant: curr.Tolerant,
                Total: curr.Total,
                count: 1,
            });
        } else {
            /*
             * Data now holds the existing data for the day. It's technically a list
             * of size one, so get the first element out. Now modify the list to add
             * our new values to the existing ones, and to increment the count.
             */
            data = data[0];
            prev[data.idx] = {
                date: curr.date,
                Sensitive: data.Sensitive + curr.Sensitive,
                'Somewhat Sensitive': data['Somewhat Sensitive'] + curr['Somewhat Sensitive'],
                Tolerant: data.Tolerant + curr.Tolerant,
                Total: data.Total + curr.Total,
                count: data.count + 1,
            }
        }
        return prev;
    }, []).map((value) => {
        /*
         * Now our list should look like this:
         *
         * [
         *   {
         *     date: '...',
         *     Sensitive: ...,
         *     'Somewhat Sensitive': ...,
         *     Tolerant: ...,
         *     Total: ...,
         *     count: ...,
         *     idx: 1,
         *   },
         *   {
         *     ...
         *   },
         *   ...
         * ]
         *
         * So, we mostly have the format we want. We just need to divide the sums
         * by the count to get our averages, and filter the counts and indexes out
         * of our data.
         */
        return {
            date: value.date,
            Sensitive: value.Sensitive / value.count,
            'Somewhat Sensitive': value['Somewhat Sensitive'] / value.count,
            Tolerant: value.Tolerant / value.count,
            Total: value.Total / value.count,
        };
    });

    formatted.sort((a, b) => {
        return (a.date < b.date ? -1 : (a.date > b.date ? 1 : 0));
    });

    columns = ['date', 'Tolerant', 'Somewhat Sensitive', 'Sensitive', 'Total'];

    const types = columns.slice(1).map((name) => {
        return {
            name: name,
            values: formatted.map((d) => {
                return {date: d.date, value: d[name]};
            }).filter(d => {
                return !isNaN(d.value);
            })
        };
    });

    const container = outerContainer;
    const margin = {top: 20, right: 200, bottom: 50, left: 40};
    const width = container.width() - margin.left - margin.right;
    const height = 250 - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .range([0, width]);

    x.domain([
        date_range[0] !== 0 ? new Date(date_range[0]) :
            d3.min(formatted, (d) => {
                return new Date(d.date) || new Date(new Date().getTime() - 86400)
            }),
        date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
            d3.max(formatted, (d) => {
                return new Date(d.date) || new Date()
            }),
    ]);
    const y = d3.scaleLinear()
        .domain([0,
            d3.max(types, (c) => {
                return d3.max(c.values, (d) => {
                    return d.value || 1; // Prevent NaNs from spoiling the max
                }) || 1
            }) || 1
        ])
        .range([height, 0]);
    const z = d3.scaleOrdinal()
        .domain(types.map((c) => {
            return c.name
        }))
        .range(['#869099', '#8c7853', '#007d4a', '#e24431']);

    const svg = d3.select('#graph-' + siteId).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    const g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    g.append('g')
        .attr('class', 'axis axis--x')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(d3.axisBottom(x))
    .selectAll("text")
        .attr("y", 5)
        .attr("x", 7)
        .attr("dy", ".35em")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");

    g.append('g')
        .attr('class', 'axis axis--y')
        .call(d3.axisLeft(y));

    if (formatted.length > 0) {
        const type = g.selectAll('.type')
            .data(types)
            .enter()
            .append('g')
            .attr('class', 'type');

        type.selectAll('dot')
            .data((d) => {
                return d.values.map((e) => {
                    e['name'] = d.name;
                    return e
                });
            })
            .enter().append('circle')
            .attr('r', 3.5)
            .attr('cx', (d) => {
                return x(new Date(d.date))
            })
            .attr('cy', (d) => {
                return y(d.value)
            })
            .style('stroke', (d) => {
                return z(d.name)
            })
            .style('fill', (d) => {
                return z(d.name)
            });

        const legend = g.selectAll('.legend')
            .data(types)
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', (d, i) => {
                return 'translate(' + (width + margin.left + 5) + ', ' + i * 20 + ')';
            })
            .style('border', '1px solid black')
            .style('font', '12px sans-serif');

        legend.append('rect')
            .attr('x', 2)
            .attr('width', 18)
            .attr('height', 2)
            .attr('fill', (d) => {
                return z(d.name);
            });

        legend.append('text')
            .attr('x', 25)
            .attr('dy', '.35em')
            .attr('text-anchor', 'begin')
            .attr('fill', (d) => {
                return z(d.name);
            })
            .text((d) => {
                return d.name;
            });
    }
};

const useBarGraph = function useBarGraph() {
    const outerContainer = $('#graph-' + siteId);
    outerContainer.find('svg').remove();
    $('.graph-header').hide();
    outerContainer.find('.graph-header').show();

    // Copy the data so we don't change the original
    data = JSON.parse(JSON.stringify(window.data_summ));

    const categories = {
        'tolerant': [],
        'somewhat': [],
        'sensitive': [],
        'total': []
    };

    let numEntries = 0;
    for (let key in data) {
        const date = parseInt(key, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        for (let category in data[key]) {
            let total = 0;
            for (let species of data[key][category]) { // Look at each animal
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

        const species = categories[category].filter(d => {
            return !isNaN(d.value);
        }).sort((a, b) => {
            return a.name.localeCompare(b.name);
        });

        const container = $('#graph-' + siteId + '-' + category);
        const margin = {top: 50, right: 100, bottom: 80, left: 50};
        const width = (Math.min(container.width(), 150 * species.length)) -
            margin.left - margin.right;
        const height = 256 - margin.top - margin.bottom;

        const x = d3.scaleBand()
            .domain(species.map((d) => {
                return d.name
            }))
            .range([0, width])
            .paddingInner(0.1);
        const y = d3.scaleLinear()
            .domain([0, d3.max(species, (d) => {
                return d.value
            }) || 1])
            .range([height, 0]);

        const xAxis = d3.axisBottom(x);
        const yAxis = d3.axisLeft(y).ticks(10);

        const svg = d3.select('#graph-' + siteId + '-' + category).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .attr('xmlns', 'http://www.w3.org/2000/svg')
            .attr('xmlns:xlink', 'http://www.w3.org/1999/xlink')
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis)
        .selectAll("text")
            .attr("y", 5)
            .attr("x", 7)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start");

        svg.append('g')
            .attr('class', 'y axis')
            .call(yAxis)
            .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 6)
            .attr('dy', '.71em')
            .style('text-anchor', 'end')
            .text('Frequency');

        if (species.length > 0) {
            svg.selectAll('.bar')
                .data(species)
                .enter()
                .append('rect')
                .attr('class', 'bar')
                .attr('x', (d) => {
                    return x(d.name)
                })
                .attr('width', x.bandwidth())
                .attr('y', (d) => {
                    return y(d.value || 0)
                })
                .attr('height', (d) => {
                    return height - y(d.value || 0)
                })
                .attr('x-data-name', (d) => {
                    return d.name
                })
                .attr('x-data-value', (d) => {
                    return d.value || 0
                });

            const hover = svg.append('g')
                .attr('class', 'bar-img')
                .attr('transform', 'translate(0,0)')
                .attr('width', 130)
                .attr('height', 65)
                .attr('opacity', 0);

            hover.append('rect')
                .attr('x', 0)
                .attr('y', 0)
                .attr('width', 130)
                .attr('height', 65)
                .attr('fill', '#ffffff')
                .attr('stroke', '#000000')
                .style('border', '1px solid black');

            hover.append('image')
                .attr('x', 0)
                .attr('y', 0)
                .attr('width', 125)
                .attr('height', 45)
                .attr('xlink:href', '/static/streamwebs/images/macroinvertebrates/macro_snail.png');

            hover.append('text')
                .attr('x', 10)
                .attr('y', 55)
                .attr('dy', '0.2em')
                .style('font', '10px sans-serif');
        }
    }

    const totals = categories['total'];
    let sum = 0;
    for (let total of totals) {
        sum += total.value;
    }
    const names = {
        'sensitive': 'Sensitive',
        'somewhat': 'Somewhat Sensitive',
        'tolerant': 'Tolerant'
    };
    const columns = ['Sensitive', 'Somewhat Sensitive', 'Tolerant'];

    const container = $('#graph-' + siteId + '-pie');
    const margin = {top: 20, right: 20, bottom: 30, left: 20};
    const width = Math.min(
        container.width() - margin.right - margin.left,
        768
    );
    const height = 256;
    const radius = Math.min(width, height) / 2;

    const color = d3.scaleOrdinal()
        .domain(columns)
        .range(['#007d4a', '#869099', '#8c7853']);

    const arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    const pie = d3.pie()
        .sort(null)
        .value((d) => {
            return d.value
        });

    const svg = d3.select('#graph-' + siteId + '-pie').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    const g = svg.append('g')
        .attr('transform', 'translate(' + (width / 2 + margin.left) + ',' + (height / 2 + margin.top) + ')');

    const arcs = g.selectAll('.arc')
        .data(pie(totals))
        .enter()
        .append('g')
        .attr('class', 'arc');

    arcs.append('path')
        .attr('d', arc)
        .style('fill', (d) => {
            return color(d.data.name)
        });

    const legend = svg.selectAll('.legend')
        .data(totals)
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', (d, i) => {
            return 'translate(0, ' + i * 20 + ')';
        })
        .style('font', '12px sans-serif');

    legend.append('rect')
        .attr('x', width - 18)
        .attr('width', 18)
        .attr('height', 18)
        .attr('fill', (d) => {
            return color(d.name);
        });

    legend.append('text')
        .attr('x', width - 24)
        .attr('y', 9)
        .attr('dy', '.35em')
        .attr('text-anchor', 'end')
        .text((d) => {
            return names[d.name] + ' (' + toFixed(((d.value / sum) * 100), 2) + '%)';
        });

    $('.bar').mouseenter((e) => {
        const target = $(e.target);
        const g = target.siblings('.bar-img');
        g.find('image')[0].setAttributeNS('http://www.w3.org/1999/xlink', 'href',
            '/static/streamwebs/images/macroinvertebrates/macro_' +
            target.attr('x-data-name').toLowerCase().replace(/[ /]/g, '_') +
            '.png'
        );
        g.attr('transform',
            'translate(' +
            (parseFloat(target.attr('x')) + parseFloat(target.attr('width')) + 10) +
            ',' + (parseFloat(target.attr('height')) + parseFloat(target.attr('y'))) / 4 + ')'
        );
        g.find('text').html(
            target.attr('x-data-name') + ' (' + toFixed(target.attr('x-data-value'), 2) + ')'
        );
        g.attr('opacity', 1);
    })
        .mouseleave((e) => {
            $(e.target).siblings('.bar-img').attr('opacity', 0);
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

        $('input[name=' + this.name + ']').each(function () {
            this.was_checked = this.checked;
        });
    }

    return this.focus(focus).change(change);
};



$(window).resize(() => {
    if ($('input[name=type]:checked').val() === 'line') {
        useLineGraph();
    } else {
        useBarGraph();
    }
});

$(() => {
    $('input[type=date]').val('');
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

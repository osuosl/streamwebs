var num_min = -9007199254740991
var num_max = 9007199254740991

var data = window.data_summ;

var date_range = [0, num_max];

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

var changeRangeStart = function changeRangeStart() {
    if (!$(this).val()) { // If the field is empty, clear the range
        date_range[0] = 0;
    } else {
        var date = Date.parse($(this).val());
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

var changeRangeEnd = function changeRangeEnd() {
    if (!$(this).val()) { // If the field is empty, clear the range
        date_range[1] = num_max;
    } else {
        var date = Date.parse($(this).val());
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

var useLineGraph = function useLineGraph() {
    var outerContainer = $('#graph-' + siteId);
    outerContainer.find('svg').remove();
    $('.graph-header').show();
    outerContainer.find('.graph-header').hide();

    // Copy the data so we don't change the original
    data = JSON.parse(JSON.stringify(window.data_time));

    var formatted = [];

    for (var key in data) {
        var date = parseInt(key, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        var total = 0;
        for (var category in data[key]) {
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
    formatted = formatted.map(function (x) {
        /*
         * First we'll map the data to remove any extraneous values just in case,
         * and to change the date to a string of just the date.
         */
        var key = x.date.toISOString().substring(0, 10);

        return {
            date: key,
            Sensitive: x.Sensitive,
            'Somewhat Sensitive': x['Somewhat Sensitive'],
            Tolerant: x.Tolerant,
            Total: x.Total,
        };
    }).reduce(function (prev, curr) {
        /*
         * Next, we'll reduce it down to sums per day.
         */

        /*
         * `data` here represents the existing data for the day we're looking at,
         * if it exists. It contains all of the sums we've already calculated for
         * this day, plus its own index in the list so we can find it later.
         */
        var data = prev.map(function (x, i) {
            x['idx'] = i;
            return x;
        })
        .filter(function (x) {
            d1 = new Date(x.date);
            d2 = new Date(curr.date);
            return d1.getTime() === d2.getTime();
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
    }, []).map(function (value) {
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

    formatted.sort(function (a, b) {
        return (a.date < b.date ? -1 : (a.date > b.date ? 1 : 0));
    });

    columns = ['date', 'Tolerant', 'Somewhat Sensitive', 'Sensitive', 'Total'];

    var types = columns.slice(1).map(function (name) {
        return {
            name: name,
            values: formatted.map(function (d) {
                return {date: d.date, value: d[name]};
            }).filter(function (d) {
                return !isNaN(d.value);
            })
        };
    });

    var container = outerContainer;
    var margin = {top: 20, right: 40, bottom: 50, left: 40};
    var width = container.width() - margin.left - margin.right;
    var height = 320 - margin.top - margin.bottom;

    var x = d3.scaleTime()
        .range([0, width]);

    x.domain([
        date_range[0] !== 0 ? new Date(date_range[0]) :
            d3.min(formatted, function (d) {
                return new Date(d.date) || new Date(new Date().getTime() - 86400);
            }),
        date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
            d3.max(formatted, function (d) {
                return new Date(d.date) || new Date();
            }),
    ]);
    var y = d3.scaleLinear()
        .domain([0,
            d3.max(types, function (c) {
                return d3.max(c.values, function (d) {
                    return d.value || 1; // Prevent NaNs from spoiling the max
                }) || 1;
            }) || 1
        ])
        .range([height, 0]);
    var z = d3.scaleOrdinal()
        .domain(types.map(function (c) {
            return c.name;
        }))
        .range(['#869099', '#8c7853', '#007d4a', '#e24431']);

    var svg = d3.select('#graph-' + siteId).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom + 100);

    var g = svg.append('g')
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
        var type = g.selectAll('.type')
            .data(types)
            .enter()
            .append('g')
            .attr('class', 'type');

        type.selectAll('dot')
            .data(function (d) {
                return d.values.map(function (e) {
                    e['name'] = d.name;
                    return e;
                });
            })
            .enter().append('circle')
            .attr('r', 3.5)
            .attr('cx', function (d) {
                return x(new Date(d.date));
            })
            .attr('cy', function (d) {
                return y(d.value);
            })
            .style('stroke', function (d) {
                return z(d.name);
            })
            .style('fill', function (d) {
                return z(d.name);
            });

        var line = d3.line()
            .x(function(d) {
                return x(new Date(d.date));
            })
            .y(function(d) {
                return y(d.value);
            });

        type.selectAll('svg g')
            .data(types)
            .enter().append('path')
            .attr('class', 'line')
            .attr('d', function(d) { return line(d.values); })
            .style('stroke', function(d) {
              return z(d.name);
            });

        var legend = g.selectAll('.legend')
            .data(types)
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function (d, i) {
                return 'translate(' + margin.left + ', ' +
                    (height + margin.top + margin.bottom + i * 20) + ')';
            })
            .style('border', '1px solid black')
            .style('font', '12px sans-serif');

        legend.append('rect')
            .attr('x', 2)
            .attr('width', 18)
            .attr('height', 2)
            .attr('fill', function (d) {
                return z(d.name);
            });

        legend.append('text')
            .attr('x', 25)
            .attr('dy', '.35em')
            .attr('text-anchor', 'begin')
            .attr('fill', function (d) {
                return z(d.name);
            })
            .text(function (d) {
                return d.name;
            });
    }
};

var useBarGraph = function useBarGraph() {
    var outerContainer = $('#graph-' + siteId);
    outerContainer.find('svg').remove();
    $('.graph-header').hide();
    outerContainer.find('.graph-header').show();

    // Copy the data so we don't change the original
    data = JSON.parse(JSON.stringify(window.data_summ));

    var categories = {
        'tolerant': [],
        'somewhat': [],
        'sensitive': [],
        'total': []
    };

    var numEntries = 0;
    for (var key in data) {
        var date = parseInt(key, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        for (var category in data[key]) {
            var total = 0;
            for (var species of data[key][category]) { // Look at each animal
                var found = false;
                for (var entry of categories[category]) {
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

            var found = false;
            for (var entry of categories['total']) {
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

    for (var category in categories) {
        for (var entry of categories[category]) {
            entry.value /= numEntries; // Earlier summed, now divide to get average
            entry.value = Math.trunc(entry.value);
        }
    }

    for (var category in categories) {
        if (category == 'total') {
            continue;
        }

        var species = categories[category].filter(function (d) {
            return !isNaN(d.value);
        }).sort(function (a, b){
            return a.name.localeCompare(b.name);
        });

        var container = $('#graph-' + siteId + '-' + category);
        var margin = {top: 50, right: 100, bottom: 80, left: 50};
        var width = (Math.min(container.width(), 150 * species.length)) -
            margin.left - margin.right;
        var height = 256 - margin.top - margin.bottom;

        var x = d3.scaleBand()
            .domain(species.map(function (d) {
                return d.name;
            }))
            .range([0, width])
            .paddingInner(0.1);
        var y = d3.scaleLinear()
            .domain([0, d3.max(species, function (d) {
                return d.value;
            }) || 1])
            .range([height, 0]);

        var xAxis = d3.axisBottom(x);
        var yAxis = d3.axisLeft(y).ticks(10);

        var svg = d3.select('#graph-' + siteId + '-' + category).append('svg')
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
                .attr('x', function (d) {
                    return x(d.name);
                })
                .attr('width', x.bandwidth())
                .attr('y', function (d) {
                    return y(d.value || 0);
                })
                .attr('height', function (d) {
                    return height - y(d.value || 0);
                })
                .attr('x-data-name', function (d) {
                    return d.name;
                })
                .attr('x-data-value', function (d) {
                    return d.value || 0;
                });

            var hover = svg.append('g')
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

    var totals = categories['total'];
    var sum = 0;
    for (var total of totals) {
        sum += total.value;
    }
    var names = {
        'sensitive': 'Sensitive',
        'somewhat': 'Somewhat Sensitive',
        'tolerant': 'Tolerant'
    };
    var columns = ['Sensitive', 'Somewhat Sensitive', 'Tolerant'];

    var container = $('#graph-' + siteId + '-pie');
    var margin = {top: 20, right: 20, bottom: 30, left: 20};
    var width = Math.min(
        container.width() - margin.right - margin.left,
        768
    );
    var height = 256;
    var radius = Math.min(width, height) / 2;

    var color = d3.scaleOrdinal()
        .domain(columns)
        .range(['#007d4a', '#869099', '#8c7853']);

    var arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var pie = d3.pie()
        .sort(null)
        .value(function (d) {
            return d.value;
        });

    var svg = d3.select('#graph-' + siteId + '-pie').append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    var g = svg.append('g')
        .attr('transform', 'translate(' + (width / 2 + margin.left) + ',' + (height / 2 + margin.top) + ')');

    var arcs = g.selectAll('.arc')
        .data(pie(totals))
        .enter()
        .append('g')
        .attr('class', 'arc');

    arcs.append('path')
        .attr('d', arc)
        .style('fill', function (d) {
            return color(d.data.name);
        });

    var legend = svg.selectAll('.legend')
        .data(totals)
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function (d, i) {
            return 'translate(0, ' + i * 20 + ')';
        })
        .style('font', '12px sans-serif');

    legend.append('rect')
        .attr('x', width - 18)
        .attr('width', 18)
        .attr('height', 18)
        .attr('fill', function (d) {
            return color(d.name);
        });

    legend.append('text')
        .attr('x', width - 24)
        .attr('y', 9)
        .attr('dy', '.35em')
        .attr('text-anchor', 'end')
        .text(function (d) {
            return names[d.name] + ' (' + toFixed(((d.value / sum) * 100), 2) + '%)';
        });

    $('.bar').mouseenter(function (e) {
        var target = $(e.target);
        var g = target.siblings('.bar-img');
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
        .mouseleave(function (e) {
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



$(window).resize(function () {
    if ($('input[name=type]:checked').val() === 'line') {
        useLineGraph();
    } else {
        useBarGraph();
    }
});

var addDateRange = function addDateRange() {
    console.log(window.data_time);
    var count = 0;
    for (key in window.data_time) {
        count++;
    }
    if (count > 0) {
        var first = 1;
        var min, max;
        for (key in window.data_time) {
            if (first == 1) {
                var min = key;
                var max = key;
                first--;
            }
            else {
                if (key < min) min = key;
                if (key > max) max = key;
            }
        }
        var min_date = new Date(0);
        var max_date = new Date(0);
        min_date.setUTCSeconds(min);
        max_date.setUTCSeconds(max);
        var date_range = "";
        var date_range = date_range + min_date.getFullYear().toString()
            + "-" + min_date.getDate().toString() + "-" + (min_date.getMonth() + 1).toString()
            + " ~ " + max_date.getFullYear().toString()
            + "-" + max_date.getDate().toString() + "-" + (max_date.getMonth() + 1).toString()
        $('p.date-range').text('Date range of data: ' + date_range);
    }
}

$(function () {
    $('input[type=date]').val('');
    $('#date-start').change(changeRangeStart);
    $('#date-end').change(changeRangeEnd);
    addDateRange();
    $('input[type=radio]').fix_radios();
    $('input[name=type]').change(function () {
        if ($('input[name=type]:checked').val() === 'line') {
            useLineGraph();
        } else {
            useBarGraph();
        }
    });

    $('#type-bar').change();
});

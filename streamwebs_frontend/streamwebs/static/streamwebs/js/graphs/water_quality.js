/*******************************************************************************
 *******************************************************************************
 *
 * Date ranges
 *
 *******************************************************************************
 ******************************************************************************/

let date_range = [Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER];

const changeRangeStart = function changeRangeStart() {
    if (!$(this).val()) { // If the field is empty, clear the range
        date_range[0] = Number.MIN_SAFE_INTEGER;
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

/*******************************************************************************
 *******************************************************************************
 *
 * Histogram
 *
 *******************************************************************************
 ******************************************************************************/

const showHistogram = function showMouseover(e) {

};

/*******************************************************************************
 *******************************************************************************
 *
 * Mouseover
 *
 *******************************************************************************
 ******************************************************************************/

const showMouseover = function showMouseover(e) {

};

const hideMouseover = function hideMouseover(e) {

};

/*******************************************************************************
 *******************************************************************************
 *
 * Line graphs
 *
 *******************************************************************************
 ******************************************************************************/

let types1 = {}, types2 = {}, filtered1 = {}, filtered2 = {};

const formatData = function formatData(data, key) {
    /*
     * So we currently have a list of data points, each one containing a date
     * and a list of 4 samples, each sample having one each of every data type
     * we need. Instead, we want to pull out just one type per data point, pair
     * it with the date, and average each day into one point.
     */
    return data.map(d => {
        /*
         * Turn each data point *d*, which looks like this:
         *
         * {
         *  date: ...,
         *  samples: [
         *    {
         *      water_temperature: ...,
         *      ...
         *    },
         *    ...
         *  ],
         *  ...
         * }
         *
         * into just a date-value pair.
         */
        return {
            date: d.date,
            /*
             * Take our samples, and reduce it into a single average for a value.
             */
            value: d.samples.reduce((prev, curr, idx) => {
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
            }, 0),
        };
    }).filter(d => {
        return !isNaN(d.value);
    });
};

const filterOutliers = function filterOutliers(entries) {

    /*
     * Next we calculate the first and third quartile and the inter-quartile range
     */

    const points = entries.map(d => {
        return d.value;
    }).sort();
    const n = points.length;

    const firstQP = Math.floor(.25*(n+1));

    const firstQ = .25*(n+1) === firstQP ? // If (n+1)/4 is an integer
        points[.25*(n+1)] : // Use it as the index
        // Otherwise, interpolate the two values, using
        // x[int((n+1)/4)] + x[int((n+1)/4)+1](decimal((n+1)/4))
        points[firstQP] + (points[firstQP+1] * (.25*(n+1) - firstQP));

    const thirdQP = Math.floor(.75*(n+1));

    const thirdQ = .25*(n+1) === thirdQP ? // If 3(n+1)/4 is an integer
        points[thirdQP] : // Use it as the index
        // Otherwise, interpolate the two values, using
        // x[int(3(n+1)/4)] + x[int(3(n+1)/4)+1](decimal(3(n+1)/4))
        points[thirdQP] + (points[thirdQP+1] * (.75*(n+1) - thirdQP));

    const iqr = thirdQ - firstQ;

    /*
     * Finally, we filter outliers (values more than 1.5*IQR away from the quartiles),
     * then average the remaining data points.
     */

    return entries.filter(d => {
        return d.value >= firstQ - (1.5*iqr) &&
               d.value <= thirdQ + (1.5*iqr);
    /*
     * Get the averages by each day. For more information, see lines 134-213
     * of macros.js.
     */
    }).reduce((prev, curr) => {
        let data = prev.map((x, i) => {
            x['idx'] = i;
            return x;
        }).filter(x => {
            return x.date.getTime() === curr.date.getTime();
        });

        if (!data || data === [] || data.length === 0) {
            prev.push({
                date: curr.date,
                value: curr.value,
                count: 1,
            });
        } else {
            data = data[0];
            prev[data.idx] = {
                date: curr.date,
                value: data.value + curr.value,
                count: data.count + 1,
            }
        }
        return prev;
    }, []).map(x => {
        return {
            date: x.date,
            value: x.value / x.count,
        }
    });
};

const margin = {top: 20, right: 150, bottom: 50, left: 40};
const defineWidth = function defineWidth(container) {
    return container.width() - (margin.right + margin.left);
};

const defineHeight = function defineHeight() {
    return 300 - (margin.top + margin.bottom);
};

const createGraphTemplate = function createGraphTemplate(container, width, height, x, y) {
    const svg1 = d3.select(container).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .style('border', '1px solid #808080');

    const g1 = svg1.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    g1.append('g')
        .attr('class', 'axis axis--x x')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(d3.axisBottom(x))
    .selectAll("text")
        .attr("y", 5)
        .attr("x", 7)
        .attr("dy", ".35em")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");

    g1.append('g')
        .attr('class', 'axis axis--y y')
        .call(d3.axisLeft(y));

    return g1;
};

const isGoodNum = function isGoodNum(n) {
    // NaN is not equal to itself
    return (typeof n === 'number') && n === n;
};

// If a number is passed, return it.
// If null, undefined, or NaN are passed, return a boundary value.
// If `min` is truthy, return Number.MIN_SAFE_INTEGER, else Number.MAX_SAFE_INTEGER
const valNum = function valNum(n, min) {
    return isGoodNum(n) ? n : (min ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER);
};

const getXDomain = function getX(keys) {
    let min = 0;
    if (date_range[0] !== Number.MIN_SAFE_INTEGER) {
        min = new Date(date_range[0]);
    } else {
        min = new Date(keys.map(key => {
            return Math.min(
                valNum(d3.min(types1[key], d => {
                    return d.date.getTime();
                }), false),
                window.hasSiteTwo ? valNum(d3.min(types2[key], d => {
                    return d.date.getTime();
                }), false)  : Number.MAX_SAFE_INTEGER,
            );
        }).reduce((prev, curr) => {
            return Math.min(prev, curr);
        }, Number.MAX_SAFE_INTEGER));
    }

    let max = 0;
    if (date_range[1] !== Number.MAX_SAFE_INTEGER) {
        max = new Date(date_range[1]);
    } else {
        max = new Date(keys.map(key => {
            return Math.max(
                valNum(d3.max(types1[key], d => {
                    return d.date.getTime();
                }), true),
                window.hasSiteTwo ? valNum(d3.max(types2[key], d => {
                    return d.date.getTime();
                }), true) : Number.MIN_SAFE_INTEGER,
            );
        }).reduce((prev, curr) => {
            return Math.max(prev, curr);
        }, Number.MIN_SAFE_INTEGER));
    }

    return [min, max];
};

const getYDomain = function getY(keys) {
    const min = keys.map(key => {
        const min1 = valNum(d3.min(types1[key], d => {
            return valNum(d.value, false);
        }), false);
        const min2 = window.hasSiteTwo ? valNum(d3.min(types2[key], d => {
            return valNum(d.value, false);
        }), false) : Number.MAX_SAFE_INTEGER;
        return Math.min(min1, min2);
    }).reduce((prev, curr) => {
        return Math.min(prev, curr);
    }, Number.MAX_SAFE_INTEGER);

    const max = keys.map(key => {
        const max1 = valNum(d3.max(types1[key], d => {
            return valNum(d.value, true);
        }), true);
        const max2 = window.hasSiteTwo ? valNum(d3.max(types2[key], d => {
            return valNum(d.value, true);
        }), true) : Number.MIN_SAFE_INTEGER;
        return Math.max(max1, max2);
    }).reduce((prev, curr) => {
        return Math.max(prev, curr);
    }, Number.MIN_SAFE_INTEGER);

    return [min, max === min ? max+10 : max];
};

const createGraph = function createGraph() {
    const outerContainer = $('#graph-container');
    outerContainer.find('svg').remove();

    let data = JSON.parse(JSON.stringify(window.data.site1)); // Copy the data so we don't change the original

    const formatted1 = [];

    for (let datum of data) {
        const date = parseInt(datum.date, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        datum.date = new Date(date);

        formatted1.push(datum);
    }

    formatted1.sort((a, b) => {
        return a.date - b.date;
    });

    for (key of ['water_temperature', 'air_temperature', 'dissolved_oxygen',
    'pH', 'turbidity', 'salinity', 'conductivity', 'fecal_coliform', 'bod',
    'total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']) {
        types1[key] = formatData(formatted1, key);
        filtered1[key] = filterOutliers(types1[key]);
    }

    const formatted2 = [];

    if (window.hasSiteTwo) {
        data = JSON.parse(JSON.stringify(window.data.site2));
        for (let datum of data) {
            const date = parseInt(datum.date, 10) * 1000; // Convert from seconds to millis
            if (date >= date_range[1] || date <= date_range[0]) {
                continue;
            }

            datum.date = new Date(date);

            formatted2.push(datum);
        }

        formatted2.sort((a, b) => {
            return a.date - b.date;
        });

        for (key of ['water_temperature', 'air_temperature', 'dissolved_oxygen',
        'pH', 'turbidity', 'salinity', 'conductivity', 'fecal_coliform', 'bod',
        'total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']) {
            types2[key] = formatData(formatted2, key);
            filtered2[key] = filterOutliers(types2[key]);
        }
    }

    /***************************************************************************
     * Temperature
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-temperature';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-temperature';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['water_temperature', 'air_temperature']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['water_temperature', 'air_temperature']))
            .range([height, 0]);
        const z = d3.scaleOrdinal()
            .domain(['Air Temperature', 'Water Temperature'])
            .range(['#0000bf', '#bf0000']);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if ((types1.water_temperature.length ||
        types1.air_temperature.length) ||
        (window.hasSiteTwo && (types2.water_temperature.length ||
        types2.air_temperature.length))) {
            $('#temperature-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.water_temperature.length || types1.air_temperature.length) {
                const type1 = g1.selectAll('.temp')
                    .data([
                        {
                            name: "Water Temperature",
                            values: types1.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: types1.air_temperature
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'temp');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol()
                        .type(d => d.name === 'Water Temperature' ?
                                d3.symbolCircle : d3.symbolTriangle
                        )
                    )
                    .style('stroke', d => {
                        return z(d.name)
                    })
                    .style('fill', d => {
                        return z(d.name)
                    })
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);

                const legend1 = g1.selectAll('.legend')
                    .data([
                        {
                            name: "Water Temperature",
                            values: types1.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: types1.air_temperature
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'legend')
                    .attr('transform', (d, i) => {
                        return 'translate(' + (width + 10) + ', ' + i * 20 + ')';
                    })
                    .style('border', '1px solid black')
                    .style('font', '12px sans-serif');

                legend1.append('path')
                    .attr('transform', 'translate(5,0)')
                    .attr('d', d3.symbol()
                        .type(d => d.name === 'Water Temperature' ?
                                d3.symbolCircle : d3.symbolTriangle
                        ))
                    .attr('fill', d => {
                        return z(d.name);
                    });

                legend1.append('text')
                    .attr('x', 20)
                    .attr('dy', '.35em')
                    .attr('text-anchor', 'begin')
                    .attr('fill', d => {
                        return z(d.name);
                    })
                    .text(d => {
                        return d.name;
                    });
            }

            if (window.hasSiteTwo && (
                types2.water_temperature.length || types2.air_temperature.length
            )) {
                const type2 = g2.selectAll('.temp')
                    .data([
                        {
                            name: "Water Temperature",
                            values: types2.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: types2.air_temperature
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'temp');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol()
                        .type(d => d.name === 'Water Temperature' ?
                                d3.symbolCircle : d3.symbolTriangle
                        )
                    )
                    .style('stroke', d => {
                        return z(d.name)
                    })
                    .style('fill', d => {
                        return z(d.name)
                    })
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);

                const legend2 = g2.selectAll('.legend')
                    .data([
                        {
                            name: "Water Temperature",
                            values: types2.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: types2.air_temperature
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'legend')
                    .attr('transform', (d, i) => {
                        return 'translate(' + (width + 10) + ', ' + i * 20 + ')';
                    })
                    .style('border', '1px solid black')
                    .style('font', '12px sans-serif');

                legend2.append('rect')
                    .attr('x', 2)
                    .attr('width', 18)
                    .attr('height', 2)
                    .attr('fill', d => {
                        return z(d.name);
                    });

                legend2.append('text')
                    .attr('x', 25)
                    .attr('dy', '.35em')
                    .attr('text-anchor', 'begin')
                    .attr('fill', d => {
                        return z(d.name);
                    })
                    .text(d => {
                        return d.name;
                    });
            }

        } else {
            $('#temperature-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Dissolved Oxygen
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-oxygen';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-oxygen';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['dissolved_oxygen']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['dissolved_oxygen']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.dissolved_oxygen.length ||
        (window.hasSiteTwo && types2.dissolved_oxygen.length)) {
            $('#oxygen-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.dissolved_oxygen.length) {
                const type1 = g1.selectAll('.do')
                    .data([{
                        name: 'Dissolved Oxygen',
                        values: types1.dissolved_oxygen
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'do');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.dissolved_oxygen.length) {
                const type2 = g2.selectAll('.do')
                    .data([{
                        name: 'Dissolved Oxygen',
                        values: types2.dissolved_oxygen
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'do');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#oxygen-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * pH
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-ph';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-ph';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['pH']));
        const y = d3.scaleLinear()
            .domain([0, 14])
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.pH.length || (window.hasSiteTwo && types2.pH.length)) {
            $('#ph-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.pH.length) {
                const type1 = g1.selectAll('.ph')
                    .data([{
                        name: 'pH',
                        values: types1.pH
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'ph');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.pH.length) {
                const type2 = g2.selectAll('.ph')
                    .data([{
                        name: 'pH',
                        values: types2.pH
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'ph');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

        } else {
            $('#ph-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Turbidity
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-turbidity';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-turbidity';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['turbidity']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['turbidity']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.turbidity.length ||
        (window.hasSiteTwo && types2.turbidity.length)) {
            $('#turbidity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.turbidity.length) {
                const type1 = g1.selectAll('.turb')
                    .data([{
                        name: 'Turbidity',
                        values: types1.turbidity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'turb');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.turbidity.length) {

                const type2 = g2.selectAll('.turb')
                    .data([{
                        name: 'Turbidity',
                        values: types2.turbidity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'turb');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#turbidity-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Salinity
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-salinity';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-salinity';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['salinity']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['salinity']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.salinity.length ||
        (window.hasSiteTwo && types2.salinity.length)) {
            $('#salinity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.salinity.length) {
                const type1 = g1.selectAll('.sal')
                    .data([{
                        name: 'Salinity',
                        values: types1.salinity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'sal');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.salinity.length) {
                const type2 = g2.selectAll('.sal')
                    .data([{
                        name: 'Salinity',
                        values: types2.salinity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'sal');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#salinity-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Conductivity
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-conductivity';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-conductivity';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['conductivity']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['conductivity']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.conductivity.length ||
        (window.hasSiteTwo && types2.conductivity.length)) {
            $('#conductivity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.conductivity.length) {
                const type1 = g1.selectAll('.cond')
                    .data([{
                        name: 'Conductivity',
                        values: types1.conductivity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'cond');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.conductivity.length) {
                const type2 = g2.selectAll('.cond')
                    .data([{
                        name: 'Conductivity',
                        values: types2.conductivity
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'cond');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#conductivity-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Dissolved Solids
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-dissolved';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-dissolved';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']))
            .range([height, 0]);

        const z = d3.scaleOrdinal()
            .domain(['Total Solids', 'Ammonia', 'Nitrite', 'Nitrate', 'Phosphates'])
            .range(['#000000', '#bf0000', '#00bf00', '#0000bf', '#bf00bf']);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.total_solids.length ||
        (window.hasSiteTwo && types2.total_solids.length)) {
            $('#dissolved-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.total_solids.length) {
                const type = g1.selectAll('.solids')
                    .data([
                        {
                            name: "Total Solids",
                            values: types1.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: types1.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: types1.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: types1.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: types1.phosphates
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'solids');

                type.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol()
                        .type(d => {
                            switch(d.name) {
                                case "Total Solids":
                                    return d3.symbolCircle;
                                case "Ammonia":
                                    return d3.symbolTriangle;
                                case "Nitrite":
                                    return d3.symbolDiamond;
                                case "Nitrate":
                                    return d3.symbolCross;
                                case "Phosphates":
                                    return d3.symbolWye;
                            }
                        })
                    )
                    .style('stroke', d => {
                        return z(d.name)
                    })
                    .style('fill', d => {
                        return z(d.name)
                    })
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);

                const legend = g1.selectAll('.legend')
                    .data([
                        {
                            name: "Total Solids",
                            values: types1.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: types1.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: types1.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: types1.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: types1.phosphates
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'legend')
                    .attr('transform', (d, i) => {
                        return 'translate(' + (width + 10) + ', ' + i * 20 + ')';
                    })
                    .style('border', '1px solid black')
                    .style('font', '12px sans-serif');

                legend.append('path')
                    .attr('transform', 'translate(30,0)')
                    .attr('d',  d3.symbol()
                        .type(d => {
                            switch(d.name) {
                                case "Total Solids":
                                    return d3.symbolCircle;
                                case "Ammonia":
                                    return d3.symbolTriangle;
                                case "Nitrite":
                                    return d3.symbolDiamond;
                                case "Nitrate":
                                    return d3.symbolCross;
                                case "Phosphates":
                                    return d3.symbolWye;
                            }
                        })
                    )
                    .attr('fill', d => {
                        return z(d.name);
                    });

                legend.append('text')
                    .attr('x', 40)
                    .attr('dy', '.35em')
                    .attr('text-anchor', 'begin')
                    .attr('fill', d => {
                        return z(d.name);
                    })
                    .text(d => {
                        return d.name;
                    });
            }

            if (window.hasSiteTwo && types2.total_solids.length) {
                const type = g2.selectAll('.solids')
                    .data([
                        {
                            name: "Total Solids",
                            values: types2.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: types2.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: types2.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: types2.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: types2.phosphates
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'solids');

                type.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('circle')
                    .attr('r', 3.5)
                    .attr('cx', d => {
                        return x(new Date(d.date))
                    })
                    .attr('cy', d => {
                        return y(d.value)
                    })
                    .style('stroke', d => {
                        return z(d.name)
                    })
                    .style('fill', d => {
                        return z(d.name)
                    })
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);

                const legend = g2.selectAll('.legend')
                    .data([
                        {
                            name: "Total Solids",
                            values: types2.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: types2.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: types2.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: types2.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: types2.phosphates
                        },
                    ])
                    .enter()
                    .append('g')
                    .attr('class', 'legend')
                    .attr('transform', (d, i) => {
                        return 'translate(' + (width + 10) + ', ' + i * 20 + ')';
                    })
                    .style('border', '1px solid black')
                    .style('font', '12px sans-serif');

                legend.append('rect')
                    .attr('x', 2)
                    .attr('width', 18)
                    .attr('height', 2)
                    .attr('fill', d => {
                        return z(d.name);
                    });

                legend.append('text')
                    .attr('x', 25)
                    .attr('dy', '.35em')
                    .attr('text-anchor', 'begin')
                    .attr('fill', d => {
                        return z(d.name);
                    })
                    .text(d => {
                        return d.name;
                    });
            }
        } else {
            $('#dissolved-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * BOD
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-bod';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-bod';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['bod']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['bod']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.bod.length ||
        (window.hasSiteTwo && types2.bod.length)) {
            $('#bod-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.bod.length) {
                const type1 = g1.selectAll('.bod')
                    .data([{
                        name: 'BOD',
                        values: types1.bod
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'bod');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.bod.length) {
                const type2 = g2.selectAll('.bod')
                    .data([{
                        name: 'BOD',
                        values: types2.bod
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'bod');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#bod-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Fecal Coliform
     **************************************************************************/

    {
        const containerName1 = '#graph-site1-coliform';
        const container1 = outerContainer.find(containerName1);
        const width = defineWidth(container1);
        const height = defineHeight(container1);

        const containerName2 = '#graph-site2-coliform';
        const container2 = outerContainer.find(containerName2);

        const x = d3.scaleTime()
            .range([0, width])
            .domain(getXDomain(['fecal_coliform']));
        const y = d3.scaleLinear()
            .domain(getYDomain(['fecal_coliform']))
            .range([height, 0]);

        const g1 = createGraphTemplate(containerName1, width, height, x, y);

        const g2 = createGraphTemplate(containerName2, width, height, x, y);

        if (types1.fecal_coliform.length ||
        (window.hasSiteTwo && types2.fecal_coliform.length)) {
            $('#coliform-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (types1.fecal_coliform.length) {
                const type1 = g1.selectAll('.fecal')
                    .data([{
                        name: 'Fecal Coliform',
                        values: types1.fecal_coliform
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'fecal');

                type1.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }

            if (window.hasSiteTwo && types2.fecal_coliform.length) {
                const type2 = g2.selectAll('.fecal')
                    .data([{
                        name: 'Fecal Coliform',
                        values: types2.fecal_coliform
                    }])
                    .enter()
                    .append('g')
                    .attr('class', 'fecal');

                type2.selectAll('dot')
                    .data(d => {
                        return d.values.map(e => {
                            e['name'] = d.name;
                            return e
                        });
                    })
                    .enter().append('path')
                    .attr('transform', d => {
                        return 'translate(' + x(new Date(d.date)) + ', ' +
                                y(d.value) + ')';
                    })
                    .attr('d', d3.symbol())
                    .style('stroke', '#000000')
                    .style('fill', '#000000')
                    .on('mouseover', showMouseover)
                    .on('mouseout', hideMouseover)
                    .on('click', showHistogram);
            }
        } else {
            $('#coliform-control').prop({
                disabled: 'disabled',
                checked: false
            });
            container1.css({display: 'none'});
            container2.css({display: 'none'});
        }
    }
};

/*******************************************************************************
 *******************************************************************************
 *
 * Manager
 *
 *******************************************************************************
 ******************************************************************************/

$(() => {
    $('input[type=date]').val('');
    $('#date-start').change(changeRangeStart);
    $('#date-end').change(changeRangeEnd);

    createGraph();
});

$(window).resize(() => {
    createGraph();
});

const loadSite2 = function loadSite2(site_slug) {
    $.getJSON(`/sites/${site_slug}/water/data/`, function(data) {
        if (!data.data || data.data.length === 0) {
            window.hasSiteTwo = false;
            window.data.site2 = null;
            $('#site-names').hide();
            $('#compare-error').show();
        } else {
            window.hasSiteTwo = true;
            window.data.site2 = data.data;
            $('#site2-header').text(data.site.site_name);
            $('#site-names').show();
            $('#compare-error').hide();
        }
        createGraph();
    });
};
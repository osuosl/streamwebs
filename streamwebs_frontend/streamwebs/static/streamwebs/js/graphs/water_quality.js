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
 * Mouseover
 *
 *******************************************************************************
 ******************************************************************************/

const showMouseover = function showMouseover(data) {
    const g = d3.select(this.parentElement.parentElement);
    const dotPos = [this.transform.baseVal[0].matrix['e'],
                 this.transform.baseVal[0].matrix['f']];

    const svg = d3.select(this.ownerSVGElement);
    const svgSize = [svg.attr('width'), svg.attr('height')];

    const width = 250;
    const height = 100;

    const xOffset = 120;

    const pos = [
        dotPos[0] + xOffset + width > svgSize[0] ?
            svgSize[0] - 4*width/5 : dotPos[0] + xOffset,
        dotPos[1] + height > svgSize[1] ? svgSize[1] - height - 20 : dotPos[1]
    ];

    const popup = g.append('g')
        .attr('class', 'popup')
        .attr('transform', 'translate(' + pos[0] + ',' + pos[1] + ')')
        .attr('width', width)
        .attr('height', height)
        .on('click', () => { d3.event.stopPropagation(); });

    popup.append('rect')
        .attr('x', -100)
        .attr('y', -10)
        .attr('width', width)
        .attr('height', height)
        .attr('rx', 5)
        .attr('ry', 5)
        .style('fill', '#E0E0E0')
        .style('stroke', '#000000');

    popup.append('foreignObject')
        .attr('x', -95)
        .attr('y', -5)
        .attr('width', width-10)
        .attr('height', height-10)
        .attr('text-anchor', 'middle')
        .attr('dy', '10px')
        .style('font-size', '16px')
        .style('line-height', '14px')
    .append('xhtml:div')
        .html(
            '<p>' +
                data.date.toISOString().substring(0, 10) + ': ' +
                data.value.toLocaleString('en-US', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 5,
                    style: 'decimal',
                    useGrouping: true,
                }) +
            '</p>' +
            '<p>' +
                '<a href="">View this date as a histogram</a>' +
            '</p>'
        );

    d3.event.stopPropagation();
};

const hideMouseover = function hideMouseover() {
    $('.popup').remove();
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
    }).sort((a, b) => {
        return a-b;
    });
    const n = points.length;

    /*
     * Split the array into a top and bottom half.
     * In an odd-length array, we drop the middle.
     *
     * Examples:
     * n = 12, n/2 = 6 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
     * bottom = [0, 1, 2, 3, 4, 5] = slice(0, 6) = slice(0, n/2)
     * top = [6, 7, 8, 9, 10, 11] = slice(6, 12) = slice(n/2, n)
     *
     * n = 13, n/2 = 6.5 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
     * bottom = [0, 1, 2, 3, 4, 5] = slice(0, 6) = slice(0, floor(n/2))
     * top = [7, 8, 9, 10, 11, 12] = slice(7, 13) = slice(ceil(n/2), n)
     */
    const bottom = points.slice(0, Math.floor(n/2));
    const top = points.slice(Math.ceil(n/2), n);

    /*
     * Now each quartile is the median of each array.
     * In an odd-length array, it's the halfway point of the array, which
     * (in a 0-indexed system) is floor(n/2).
     * In an even-length array, it's the average of the two points in the middle,
     * which are floor(n/2 - 1) and floor(n/2) (sum them and divide by two).
     */

    const firstQP = Math.floor(bottom.length/2);
    const firstQ = bottom.length % 2 === 0 ?
        (bottom[firstQP-1] + bottom[firstQP])/2 :
        bottom[firstQP];

    const thirdQP = Math.floor(top.length/2);
    const thirdQ = top.length % 2 === 0 ?
        (top[thirdQP-1] + top[thirdQP])/2 :
        top[thirdQP];

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
                valNum(d3.min(filtered1[key], d => {
                    return d.date.getTime();
                }), false),
                window.hasSiteTwo ? valNum(d3.min(filtered2[key], d => {
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
                valNum(d3.max(filtered1[key], d => {
                    return d.date.getTime();
                }), true),
                window.hasSiteTwo ? valNum(d3.max(filtered2[key], d => {
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
        const min1 = valNum(d3.min(filtered1[key], d => {
            return valNum(d.value, false);
        }), false);
        const min2 = window.hasSiteTwo ? valNum(d3.min(filtered2[key], d => {
            return valNum(d.value, false);
        }), false) : Number.MAX_SAFE_INTEGER;
        return Math.min(min1, min2);
    }).reduce((prev, curr) => {
        return Math.min(prev, curr);
    }, Number.MAX_SAFE_INTEGER);

    const max = keys.map(key => {
        const max1 = valNum(d3.max(filtered1[key], d => {
            return valNum(d.value, true);
        }), true);
        const max2 = window.hasSiteTwo ? valNum(d3.max(filtered2[key], d => {
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

        if ((filtered1.water_temperature.length ||
        filtered1.air_temperature.length) ||
        (window.hasSiteTwo && (filtered2.water_temperature.length ||
        filtered2.air_temperature.length))) {
            $('#temperature-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.water_temperature.length || filtered1.air_temperature.length) {
                const type1 = g1.selectAll('.temp')
                    .data([
                        {
                            name: "Water Temperature",
                            values: filtered1.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: filtered1.air_temperature
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);

                const legend1 = g1.selectAll('.legend')
                    .data([
                        {
                            name: "Water Temperature",
                            values: filtered1.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: filtered1.air_temperature
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
                filtered2.water_temperature.length || filtered2.air_temperature.length
            )) {
                const type2 = g2.selectAll('.temp')
                    .data([
                        {
                            name: "Water Temperature",
                            values: filtered2.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: filtered2.air_temperature
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);

                const legend2 = g2.selectAll('.legend')
                    .data([
                        {
                            name: "Water Temperature",
                            values: filtered2.water_temperature
                        },
                        {
                            name: "Air Temperature",
                            values: filtered2.air_temperature
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

        if (filtered1.dissolved_oxygen.length ||
        (window.hasSiteTwo && filtered2.dissolved_oxygen.length)) {
            $('#oxygen-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.dissolved_oxygen.length) {
                const type1 = g1.selectAll('.do')
                    .data([{
                        name: 'Dissolved Oxygen',
                        values: filtered1.dissolved_oxygen
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.dissolved_oxygen.length) {
                const type2 = g2.selectAll('.do')
                    .data([{
                        name: 'Dissolved Oxygen',
                        values: filtered2.dissolved_oxygen
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.pH.length || (window.hasSiteTwo && filtered2.pH.length)) {
            $('#ph-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.pH.length) {
                const type1 = g1.selectAll('.ph')
                    .data([{
                        name: 'pH',
                        values: filtered1.pH
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.pH.length) {
                const type2 = g2.selectAll('.ph')
                    .data([{
                        name: 'pH',
                        values: filtered2.pH
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.turbidity.length ||
        (window.hasSiteTwo && filtered2.turbidity.length)) {
            $('#turbidity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.turbidity.length) {
                const type1 = g1.selectAll('.turb')
                    .data([{
                        name: 'Turbidity',
                        values: filtered1.turbidity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.turbidity.length) {

                const type2 = g2.selectAll('.turb')
                    .data([{
                        name: 'Turbidity',
                        values: filtered2.turbidity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.salinity.length ||
        (window.hasSiteTwo && filtered2.salinity.length)) {
            $('#salinity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.salinity.length) {
                const type1 = g1.selectAll('.sal')
                    .data([{
                        name: 'Salinity',
                        values: filtered1.salinity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.salinity.length) {
                const type2 = g2.selectAll('.sal')
                    .data([{
                        name: 'Salinity',
                        values: filtered2.salinity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.conductivity.length ||
        (window.hasSiteTwo && filtered2.conductivity.length)) {
            $('#conductivity-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.conductivity.length) {
                const type1 = g1.selectAll('.cond')
                    .data([{
                        name: 'Conductivity',
                        values: filtered1.conductivity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.conductivity.length) {
                const type2 = g2.selectAll('.cond')
                    .data([{
                        name: 'Conductivity',
                        values: filtered2.conductivity
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.total_solids.length ||
        (window.hasSiteTwo && filtered2.total_solids.length)) {
            $('#dissolved-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.total_solids.length) {
                const type = g1.selectAll('.solids')
                    .data([
                        {
                            name: "Total Solids",
                            values: filtered1.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: filtered1.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: filtered1.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: filtered1.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: filtered1.phosphates
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);

                const legend = g1.selectAll('.legend')
                    .data([
                        {
                            name: "Total Solids",
                            values: filtered1.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: filtered1.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: filtered1.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: filtered1.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: filtered1.phosphates
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

            if (window.hasSiteTwo && filtered2.total_solids.length) {
                const type = g2.selectAll('.solids')
                    .data([
                        {
                            name: "Total Solids",
                            values: filtered2.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: filtered2.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: filtered2.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: filtered2.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: filtered2.phosphates
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);

                const legend = g2.selectAll('.legend')
                    .data([
                        {
                            name: "Total Solids",
                            values: filtered2.total_solids
                        },
                        {
                            name: "Ammonia",
                            values: filtered2.ammonia
                        },
                        {
                            name: "Nitrite",
                            values: filtered2.nitrite
                        },
                        {
                            name: "Nitrate",
                            values: filtered2.nitrate
                        },
                        {
                            name: "Phosphates",
                            values: filtered2.phosphates
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

        if (filtered1.bod.length ||
        (window.hasSiteTwo && filtered2.bod.length)) {
            $('#bod-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.bod.length) {
                const type1 = g1.selectAll('.bod')
                    .data([{
                        name: 'BOD',
                        values: filtered1.bod
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.bod.length) {
                const type2 = g2.selectAll('.bod')
                    .data([{
                        name: 'BOD',
                        values: filtered2.bod
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

        if (filtered1.fecal_coliform.length ||
        (window.hasSiteTwo && filtered2.fecal_coliform.length)) {
            $('#coliform-control').prop({
                disabled: null,
                checked: true
            });
            container1.css({display: 'block'});
            container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

            if (filtered1.fecal_coliform.length) {
                const type1 = g1.selectAll('.fecal')
                    .data([{
                        name: 'Fecal Coliform',
                        values: filtered1.fecal_coliform
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
            }

            if (window.hasSiteTwo && filtered2.fecal_coliform.length) {
                const type2 = g2.selectAll('.fecal')
                    .data([{
                        name: 'Fecal Coliform',
                        values: filtered2.fecal_coliform
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
                    .style('cursor', 'pointer')
                    .on('click', showMouseover);
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

    document.addEventListener('click', hideMouseover);

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
/*******************************************************************************
 *******************************************************************************
 *
 * Date ranges
 *
 *******************************************************************************
 ******************************************************************************/
var num_min = -9007199254740991
var num_max = 9007199254740991
var date_range = [num_min, num_max];
var outerContainer = $('#graph-container');
var hasPopup = false;

function search() {
    if($('div.search-results').css('display') == 'none'){
      $('div.search-results').show();
    }
    var search_value = $('#search').val().toLowerCase();

    dropdownShown = 0;

    $('.search-item').each(function () {
        var name = $(this).text().toLowerCase();
        var search_point = $('#search').offset().top + parseInt($('#search').css('height'));

        if (search_value && name.includes(search_value)) {
            $(this).removeClass('hide');
            $(this).css("top", search_point + (dropdownShown * 40));
            $(this).css("left", $('#search').offset().left);
            dropdownShown += 1;
        } else {
            $(this).addClass('hide');
        }
    });
}

var changeRangeStart = function changeRangeStart() {
    if (!$('#date-start').val()) { // If the field is empty, clear the range
        date_range[0] = num_min;
    } else {
        var date = Date.parse($('#date-start').val());
        if (!date || Number.isNaN(date)) {
            return;
        }

        date_range[0] = date;
    }

    createGraph();
};

var changeRangeEnd = function changeRangeEnd() {
    if (!$('#date-end').val()) { // If the field is empty, clear the range
        date_range[1] = num_max;
    } else {
        var date = Date.parse($('#date-end').val());
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

leavePopup = false;
leavePopup = false;

var showMouseover = function showMouseover(data) {
    $('.popup').remove();
    var g = d3.select(this.parentElement.parentElement);
    var dotPos = [this.transform.baseVal[0].matrix['e'],
                 this.transform.baseVal[0].matrix['f']];

    var svg = d3.select(this.ownerSVGElement);
    var svgSize = [svg.attr('width'), svg.attr('height')];

    var width = 250;
    var height = 150;

    var xOffset = 120;

    var pos = [
        dotPos[0] + xOffset + width > svgSize[0] ?
            svgSize[0] - 4*width/5 : dotPos[0] + xOffset,
        dotPos[1] + height > svgSize[1] ? svgSize[1] - height - 20 : dotPos[1]
    ];

    var popup = g.append('g')
        .attr('class', 'popup')
        .attr('transform', 'translate(' + pos[0] + ',' + pos[1] + ')')
        .attr('width', width)
        .attr('height', height)
        .on('click', function () {
             d3.event.stopPropagation();
         });

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
        .attr('x', -90)
        .attr('y', -5)
        .attr('width', width-10)
        .attr('height', height-10)
        .attr('text-anchor', 'middle')
        .attr('dy', '10px')
        .style('font-size', '16px')
        .style('line-height', '14px')
    .append('xhtml:div')
        .html(
            '<p><b>' + data.name + '</b></p>' +
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
                data.count + (data.count > 1 ? ' entries' : ' entry') +
            '</p>' +
            '<p>' +
                '<a href="' +
                    '/sites/' + data.site + '/water/' + data.key + '/' +
                    data.date.toISOString().substring(0, 10) + '/' +
                '" target="_blank">View this date as a histogram</a>' +
            '</p>'
        );

    d3.event.stopPropagation();
};

var hideMouseover = function hideMouseover() {
    $('.popup').remove();
};

/*******************************************************************************
 *******************************************************************************
 *
 * Line graphs
 *
 *******************************************************************************
 ******************************************************************************/

var types1 = {}, types2 = {}, filtered1 = {}, filtered2 = {};

var formatData = function formatData(data, key) {
    /*
     * So we currently have a list of data points, each one containing a date
     * and a list of 4 samples, each sample having one each of every data type
     * we need. Instead, we want to pull out just one type per data point, pair
     * it with the date, and average each day into one point.
     */
    return data.map(function(d) {
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
            value: d.samples.reduce(function (prev, curr, idx) {
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
    }).filter(function (d) {
        return !isNaN(d.value);
    });
};

var filterOutliers = function filterOutliers(entries) {

    /*
     * Next we calculate the first and third quartile and the inter-quartile range
     */

    var points = entries.map(function(d) {
        return d.value;
    }).sort(function (a, b) {
        return a-b;
    });
    var n = points.length;

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
    var bottom = points.slice(0, Math.floor(n/2));
    var top = points.slice(Math.ceil(n/2), n);

    /*
     * Now each quartile is the median of each array.
     * In an odd-length array, it's the halfway point of the array, which
     * (in a 0-indexed system) is floor(n/2).
     * In an even-length array, it's the average of the two points in the middle,
     * which are floor(n/2 - 1) and floor(n/2) (sum them and divide by two).
     */

    var firstQP = Math.floor(bottom.length/2);
    var firstQ = bottom.length % 2 === 0 ?
        (bottom[firstQP-1] + bottom[firstQP])/2 :
        bottom[firstQP];

    var thirdQP = Math.floor(top.length/2);
    var thirdQ = top.length % 2 === 0 ?
        (top[thirdQP-1] + top[thirdQP])/2 :
        top[thirdQP];

    var iqr = thirdQ - firstQ;

    /*
     * Finally, we filter outliers (values more than 1.5*IQR away from the quartiles),
     * then average the remaining data points.
     */

    return entries.filter(function (d) {
        return d.value >= firstQ - (1.5*iqr) &&
               d.value <= thirdQ + (1.5*iqr);
    /*
     * Get the averages by each day. For more information, see lines 134-213
     * of macros.js.
     */
 }).reduce(function (prev, curr) {
        var data = prev.map(function (x, i) {
            x['idx'] = i;
            return x;
        }).filter(function (x) {
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
    }, []).map(function (x) {
        return {
            date: x.date,
            value: x.value / x.count,
            count: x.count,
        };
    });
};

var margin = {top: 20, right: 20, bottom: 50, left: 40};
var defineWidth = function defineWidth(container) {
    return container.width() - (margin.right + margin.left);
};

var defineHeight = function defineHeight() {
    return 300 - (margin.top + margin.bottom);
};

var createGraphTemplate = function createGraphTemplate(container, width, height, x, y, extraHeight = 0) {
    var svg1 = d3.select(container).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom + extraHeight)
        .style('border', '1px solid #808080');

    var g1 = svg1.append('g')
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

var filterZeroData = function filterZeroData(filtered, key) {
    if (key === "dissolved_oxygen") {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value >= 0 && dataPoint.value <= 13 ;
        });
    }
    else if (key === "pH") {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value > 0 && dataPoint.value < 14 ;
        });
    }
    else if (key === "water_temperature") {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value >= 32 && dataPoint.value <= 140 ;
        });
    }
    else if (key === "air_temperature") {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value >= 0 && dataPoint.value <= 140 ;
        });
    }
    else if (key === "turbidity") {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value > 0;
        });
    }
    else {
        filtered = filtered.filter(function(dataPoint) {
            return dataPoint.value >= 0;
        });
    }

    return filtered;
}

var isGoodNum = function isGoodNum(n) {
    // NaN is not equal to itself
    return (typeof n === 'number') && n === n;
};

// If a number is passed, return it.
// If null, undefined, or NaN are passed, return a boundary value.
// If `min` is truthy, return num_min, else num_max
var valNum = function valNum(n, min) {
    return isGoodNum(n) ? n : (min ? num_min : num_max);
};

var getXDomain = function getX(keys) {
    var min = 0;
    if (date_range[0] !== num_min) {
        min = new Date(date_range[0]);
    } else {
        min = new Date(keys.map(function (key) {
            return Math.min(
                valNum(d3.min(filtered1[key], function (d) {
                    return d.date.getTime();
                }), false),
                window.hasSiteTwo ? valNum(d3.min(filtered2[key], function (d) {
                    return d.date.getTime();
                }), false)  : num_max
            );
        }).reduce(function (prev, curr) {
            return Math.min(prev, curr);
        }, num_max));
    }

    var max = 0;
    if (date_range[1] !== num_max) {
        max = new Date(date_range[1]);
    } else {
        max = new Date(keys.map(function (key) {
            return Math.max(
                valNum(d3.max(filtered1[key], function (d) {
                    return d.date.getTime();
                }), true),
                window.hasSiteTwo ? valNum(d3.max(filtered2[key], function (d) {
                    return d.date.getTime();
                }), true) : num_min
            );
        }).reduce(function (prev, curr) {
            return Math.max(prev, curr);
        }, num_min));
    }

    return [min, max];
};

var getYDomain = function getY(keys) {
    var min = keys.map(function (key) {
        var min1 = valNum(d3.min(filtered1[key], function (d) {
            return valNum(d.value, false);
        }), false);
        var min2 = window.hasSiteTwo ? valNum(d3.min(filtered2[key], function (d) {
            return valNum(d.value, false);
        }), false) : num_max;
        return Math.min(min1, min2);
    }).reduce(function (prev, curr) {
        return Math.min(prev, curr);
    }, num_max);

    var max = keys.map(function (key) {
        var max1 = valNum(d3.max(filtered1[key], function (d) {
            return valNum(d.value, true);
        }), true);
        var max2 = window.hasSiteTwo ? valNum(d3.max(filtered2[key], function (d) {
            return valNum(d.value, true);
        }), true) : num_min;
        return Math.max(max1, max2);
    }).reduce(function (prev, curr) {
        return Math.max(prev, curr);
    }, num_min);

    return [min, max === min ? max+10 : max];
};

var createGraph = function createGraph() {
    outerContainer.find('svg').remove();

    var data = JSON.parse(JSON.stringify(window.data.site1)); // Copy the data so we don't change the original

    var formatted1 = [];

    for (var datum of data) {
        var date = parseInt(datum.date, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        datum.date = new Date(date);

        formatted1.push(datum);
    }

    formatted1.sort(function (a, b) {
        return a.date - b.date;
    });

    for (key of ['water_temperature', 'air_temperature', 'dissolved_oxygen',
    'pH', 'turbidity', 'salinity', 'conductivity', 'fecal_coliform', 'bod',
    'total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']) {
        types1[key] = formatData(formatted1, key);
        filtered1[key] = filterZeroData(types1[key], key);
        filtered1[key] = filterOutliers(filtered1[key]);
    }
    var formatted2 = [];

    if (window.hasSiteTwo) {
        data = JSON.parse(JSON.stringify(window.data.site2));
        for (var datum of data) {
            var date = parseInt(datum.date, 10) * 1000; // Convert from seconds to millis
            if (date >= date_range[1] || date <= date_range[0]) {
                continue;
            }

            datum.date = new Date(date);

            formatted2.push(datum);
        }

        formatted2.sort(function (a, b) {
            return a.date - b.date;
        });

        for (key of ['water_temperature', 'air_temperature', 'dissolved_oxygen',
        'pH', 'turbidity', 'salinity', 'conductivity', 'fecal_coliform', 'bod',
        'total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']) {
            types2[key] = formatData(formatted2, key);
            filtered2[key] = filterZeroData(types2[key], key);
            filtered2[key] = filterOutliers(filtered2[key]);
        }
    }

    var noValidData = dataIsEmpty(filtered1);
    if (noValidData) {
        $('h6#no-valid-data').show();
    }
    showDateRange(filtered1, filtered2);

    graphTemperature();
    graphOxygen();
    graphPH();
    graphTurbidity();
    graphSalinity();
    graphConductivity();
    graphDissolved();
    graphBod();
    graphColiform();
};

var dataIsEmpty = function dataIsEmpty(data) {
  var isEmpty = Object.entries(data).every(function(e, i) {
      return e[1].length === 0;
  });
  return isEmpty;
}

var showDateRange = function showDateRange(filtered1, filtered2) {
    if (dataIsEmpty(filtered1)) {
        $('p#date-range-1').hide();
    } else {
        var dateRange = getDateRange(filtered1);
        $('p#date-range-1').show();
        $('p#date-range-1').text(
            'Date range of site 1 data: ' + dateRange[0] + '~' + dateRange[1]
        );
    }

    if (dataIsEmpty(filtered2)) {
        $('p#date-range-2').hide();
    } else {
        var dateRange = getDateRange(filtered2);
        $('p#date-range-2').show();
        $('p#date-range-2').text(
            'Date range of site 2 data: ' + dateRange[0] + '~' + dateRange[1]
        );
    }
}

var getDateRange = function getDataRange(data) {
    var min, max;
    Object.entries(data).forEach(function(category) {
        category[1].forEach(function(e) {
            if (min === undefined || e.date < min) {
                min = e.date;
            }
            if (max === undefined || e.date > max) {
              max = e.date;
            }
        })
    });
    min = dateToStr(min);
    max = dateToStr(max);
    return [min, max];
}

var dateToStr = function dateToStr(date) {
    var str = "";
    var month = date.getUTCMonth() + 1;
    var day = date.getUTCDate();
    var monthStr = month < 10 ? '0' + month.toString() : month.toString();
    var dayStr = day < 10 ? '0' + day.toString() : day.toString();
    str = str + monthStr + '/' + dayStr + '/' + date.getUTCFullYear();
    return str;
}

/***************************************************************************
 * Temperature
 **************************************************************************/
var graphTemperature = function graphTemperature(responsive=false) {
    var containerName1 = '#graph-site1-temperature';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight(responsive);

    var containerName2 = '#graph-site2-temperature';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['water_temperature', 'air_temperature']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['water_temperature', 'air_temperature']))
        .range([height, 0]);
    var z = d3.scaleOrdinal()
        .domain(['Air Temperature', 'Water Temperature'])
        .range(['#0000bf', '#bf0000']);

    var numberLegends = 2;
    var legendHeight = 20 * numberLegends + 10;
    var g1 = createGraphTemplate(containerName1, width, height, x, y, legendHeight);

    var g2 = createGraphTemplate(containerName2, width, height, x, y, legendHeight);

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
            var type1 = g1.selectAll('.temp')
                .data([
                    {
                        name: "Water Temperature",
                        key: 'water_temperature',
                        values: filtered1.water_temperature
                    },
                    {
                        name: "Air Temperature",
                        key: 'air_temperature',
                        values: filtered1.air_temperature
                    },
                ])
                .enter()
                .append('g')
                .attr('class', 'temp');
            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = d.key;
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol()
                    .type(function (d) {
                        var symbolType = d.name === 'Water Temperature' ?
                            d3.symbolCircle : d3.symbolTriangle;
                        return symbolType;
                    })
                )
                .style('stroke', function (d) {
                    return z(d.name);
                })
                .style('fill', function (d) {
                    return z(d.name);
                })
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);

            var legend1 = g1.selectAll('.legend')
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
                .attr('transform', function (d, i) {
                    return 'translate(' + 10 + ', ' + (height + 50 + i * 20) + ')';
                })
                .style('border', '1px solid black')
                .style('font', '12px sans-serif');

            legend1.append('path')
                .attr('transform', 'translate(5,0)')
                .attr('d', d3.symbol()
                    .type(function (d) {
                        var symbolType = d.name === 'Water Temperature' ?
                            d3.symbolCircle : d3.symbolTriangle;
                        return symbolType;
                    })
                )
                .attr('fill', function (d) {
                    return z(d.name);
                });

            legend1.append('text')
                .attr('x', 20)
                .attr('dy', '.35em')
                .attr('text-anchor', 'begin')
                .attr('fill', function (d) {
                    return z(d.name);
                })
                .text(function (d) {
                    return d.name;
                });
        }

        if (window.hasSiteTwo && (
            filtered2.water_temperature.length || filtered2.air_temperature.length
        )) {
            var type2 = g2.selectAll('.temp')
                .data([
                    {
                        name: "Water Temperature",
                        key: 'water_temperature',
                        values: filtered2.water_temperature
                    },
                    {
                        name: "Air Temperature",
                        key: 'air_temperature',
                        values: filtered2.air_temperature
                    },
                ])
                .enter()
                .append('g')
                .attr('class', 'temp');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = d.key;
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol()
                    .type(function (d) {
                        var symbolType = d.name === 'Water Temperature' ?
                            d3.symbolCircle : d3.symbolTriangle;
                        return symbolType;
                    })
                )
                .style('stroke', function (d) {
                    return z(d.name);
                })
                .style('fill', function (d) {
                    return z(d.name);
                })
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);

            var legend2 = g2.selectAll('.legend')
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
                .attr('transform', function (d, i) {
                    return 'translate(' + 10 + ', ' + (height + 50 + i * 20) + ')';
                })
                .style('border', '1px solid black')
                .style('font', '12px sans-serif');

            legend2.append('path')
                .attr('transform', 'translate(5,0)')
                .attr('d', d3.symbol()
                    .type(function (d) {
                        var symbolType = d.name === 'Water Temperature' ?
                            d3.symbolCircle : d3.symbolTriangle;
                        return symbolType;
                    })
                )
                .attr('fill', function (d) {
                    return z(d.name);
                });

            legend2.append('text')
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

var graphOxygen = function graphOxygen(){
    var containerName1 = '#graph-site1-oxygen';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-oxygen';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['dissolved_oxygen']));
    var y = d3.scaleLinear()
        .domain([0, 13])
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.dissolved_oxygen.length ||
    (window.hasSiteTwo && filtered2.dissolved_oxygen.length)) {
        $('#oxygen-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.dissolved_oxygen.length) {
            var type1 = g1.selectAll('.do')
                .data([{
                    name: 'Dissolved Oxygen',
                    values: filtered1.dissolved_oxygen
                }])
                .enter()
                .append('g')
                .attr('class', 'do');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'dissolved_oxygen';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.dissolved_oxygen.length) {
            var type2 = g2.selectAll('.do')
                .data([{
                    name: 'Dissolved Oxygen',
                    values: filtered2.dissolved_oxygen
                }])
                .enter()
                .append('g')
                .attr('class', 'do');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'dissolved_oxygen';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphPH = function graphPH() {
    var containerName1 = '#graph-site1-ph';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-ph';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['pH']));
    var y = d3.scaleLinear()
        .domain([0, 14])
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.pH.length || (window.hasSiteTwo && filtered2.pH.length)) {
        $('#ph-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.pH.length) {
            var type1 = g1.selectAll('.ph')
                .data([{
                    name: 'pH',
                    values: filtered1.pH,
                }])
                .enter()
                .append('g')
                .attr('class', 'ph');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'pH';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.pH.length) {
            var type2 = g2.selectAll('.ph')
                .data([{
                    name: 'pH',
                    values: filtered2.pH
                }])
                .enter()
                .append('g')
                .attr('class', 'ph');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'pH';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphTurbidity = function graphTurbidity() {
    var containerName1 = '#graph-site1-turbidity';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-turbidity';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['turbidity']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['turbidity']))
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.turbidity.length ||
    (window.hasSiteTwo && filtered2.turbidity.length)) {
        $('#turbidity-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.turbidity.length) {
            var type1 = g1.selectAll('.turb')
                .data([{
                    name: 'Turbidity',
                    values: filtered1.turbidity,
                }])
                .enter()
                .append('g')
                .attr('class', 'turb');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'turbidity';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.turbidity.length) {

            var type2 = g2.selectAll('.turb')
                .data([{
                    name: 'Turbidity',
                    values: filtered2.turbidity,
                }])
                .enter()
                .append('g')
                .attr('class', 'turb');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'turbidity';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphSalinity = function graphSalinity() {
    var containerName1 = '#graph-site1-salinity';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-salinity';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['salinity']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['salinity']))
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.salinity.length ||
    (window.hasSiteTwo && filtered2.salinity.length)) {
        $('#salinity-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.salinity.length) {
            var type1 = g1.selectAll('.sal')
                .data([{
                    name: 'Salinity',
                    values: filtered1.salinity,
                }])
                .enter()
                .append('g')
                .attr('class', 'sal');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'salinity';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.salinity.length) {
            var type2 = g2.selectAll('.sal')
                .data([{
                    name: 'Salinity',
                    values: filtered2.salinity,
                }])
                .enter()
                .append('g')
                .attr('class', 'sal');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'salinity';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphConductivity = function graphConductivity() {
    var containerName1 = '#graph-site1-conductivity';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-conductivity';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['conductivity']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['conductivity']))
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.conductivity.length ||
    (window.hasSiteTwo && filtered2.conductivity.length)) {
        $('#conductivity-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.conductivity.length) {
            var type1 = g1.selectAll('.cond')
                .data([{
                    name: 'Conductivity',
                    values: filtered1.conductivity,
                }])
                .enter()
                .append('g')
                .attr('class', 'cond');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'conductivity';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.conductivity.length) {
            var type2 = g2.selectAll('.cond')
                .data([{
                    name: 'Conductivity',
                    values: filtered2.conductivity,
                }])
                .enter()
                .append('g')
                .attr('class', 'cond');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'conductivity';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphDissolved = function graphDissolved() {
    var containerName1 = '#graph-site1-dissolved';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-dissolved';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['total_solids', 'ammonia', 'nitrite', 'nitrate', 'phosphates']))
        .range([height, 0]);

    var z = d3.scaleOrdinal()
        .domain(['Total Solids', 'Ammonia', 'Nitrite', 'Nitrate', 'Phosphates'])
        .range(['#000000', '#bf0000', '#00bf00', '#0000bf', '#bf00bf']);

    var numberLegends = 5;
    var legendHeight = 20 * numberLegends + 10;

    var g1 = createGraphTemplate(containerName1, width, height, x, y, legendHeight);

    var g2 = createGraphTemplate(containerName2, width, height, x, y, legendHeight);

    if (filtered1.total_solids.length ||
    (window.hasSiteTwo && filtered2.total_solids.length)) {
        $('#dissolved-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.total_solids.length) {
            var type = g1.selectAll('.solids')
                .data([
                    {
                        name: "Total Solids",
                        values: filtered1.total_solids,
                        key: 'total_solids',
                    },
                    {
                        name: "Ammonia",
                        values: filtered1.ammonia,
                        key: 'ammonia',
                    },
                    {
                        name: "Nitrite",
                        values: filtered1.nitrite,
                        key: 'nitrite',
                    },
                    {
                        name: "Nitrate",
                        values: filtered1.nitrate,
                        key: 'nitrate',
                    },
                    {
                        name: "Phosphates",
                        values: filtered1.phosphates,
                        key: 'phosphates',
                    },
                ])
                .enter()
                .append('g')
                .attr('class', 'solids');

            type.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = d.key;
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol()
                    .type(function (d) {
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
                .style('stroke', function (d) {
                    return z(d.name);
                })
                .style('fill', function (d) {
                    return z(d.name);
                })
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);

            var legend = g1.selectAll('.legend')
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
                .attr('transform', function (d, i) {
                    return 'translate(' + 10 + ', ' + (height + 50 + i * 20) + ')';
                })
                .style('border', '1px solid black')
                .style('font', '12px sans-serif');

            legend.append('path')
                .attr('transform', 'translate(10,0)')
                .attr('d',  d3.symbol()
                    .type(function (d) {
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
                .attr('fill', function (d) {
                    return z(d.name);
                });

            legend.append('text')
                .attr('x', 40)
                .attr('dy', '.35em')
                .attr('text-anchor', 'begin')
                .attr('fill', function (d) {
                    return z(d.name);
                })
                .text(function (d) {
                    return d.name;
                });
        }

        if (window.hasSiteTwo && filtered2.total_solids.length) {
            var type = g2.selectAll('.solids')
                .data([
                    {
                        name: "Total Solids",
                        values: filtered2.total_solids,
                        key: 'total_solids',
                    },
                    {
                        name: "Ammonia",
                        values: filtered2.ammonia,
                        key: 'ammonia',
                    },
                    {
                        name: "Nitrite",
                        values: filtered2.nitrite,
                        key: 'nitrite',
                    },
                    {
                        name: "Nitrate",
                        values: filtered2.nitrate,
                        key: 'nitrate',
                    },
                    {
                        name: "Phosphates",
                        values: filtered2.phosphates,
                        key: 'phosphates',
                    },
                ])
                .enter()
                .append('g')
                .attr('class', 'solids');

            type.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = d.key;
                        e['site'] = window.site2Id;
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
                })
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);

            var legend = g2.selectAll('.legend')
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
                .attr('transform', function (d, i) {
                    return 'translate(' + 10 + ', ' + (height + 50 + i * 20) + ')';
                })
                .style('border', '1px solid black')
                .style('font', '12px sans-serif');

            legend.append('path')
                .attr('transform', 'translate(10,0)')
                .attr('d',  d3.symbol()
                    .type(function (d) {
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

var graphBod = function graphBod() {
    var containerName1 = '#graph-site1-bod';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-bod';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['bod']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['bod']))
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.bod.length ||
    (window.hasSiteTwo && filtered2.bod.length)) {
        $('#bod-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.bod.length) {
            var type1 = g1.selectAll('.bod')
                .data([{
                    name: 'BOD',
                    values: filtered1.bod,
                }])
                .enter()
                .append('g')
                .attr('class', 'bod');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'bod';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.bod.length) {
            var type2 = g2.selectAll('.bod')
                .data([{
                    name: 'BOD',
                    values: filtered2.bod,
                }])
                .enter()
                .append('g')
                .attr('class', 'bod');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'bod';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

var graphColiform = function graphColiform() {
    var containerName1 = '#graph-site1-coliform';
    var container1 = outerContainer.find(containerName1);
    var width = defineWidth(container1);
    var height = defineHeight();

    var containerName2 = '#graph-site2-coliform';
    var container2 = outerContainer.find(containerName2);

    var x = d3.scaleTime()
        .range([0, width])
        .domain(getXDomain(['fecal_coliform']));
    var y = d3.scaleLinear()
        .domain(getYDomain(['fecal_coliform']))
        .range([height, 0]);

    var g1 = createGraphTemplate(containerName1, width, height, x, y);

    var g2 = createGraphTemplate(containerName2, width, height, x, y);

    if (filtered1.fecal_coliform.length ||
    (window.hasSiteTwo && filtered2.fecal_coliform.length)) {
        $('#coliform-control').prop({
            disabled: null,
            checked: true
        });
        container1.css({display: 'block'});
        container2.css({display: window.hasSiteTwo ? 'block' : 'none'});

        if (filtered1.fecal_coliform.length) {
            var type1 = g1.selectAll('.fecal')
                .data([{
                    name: 'Fecal Coliform',
                    values: filtered1.fecal_coliform,
                }])
                .enter()
                .append('g')
                .attr('class', 'fecal');

            type1.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'fecal_coliform';
                        e['site'] = siteId;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
        }

        if (window.hasSiteTwo && filtered2.fecal_coliform.length) {
            var type2 = g2.selectAll('.fecal')
                .data([{
                    name: 'Fecal Coliform',
                    values: filtered2.fecal_coliform,
                }])
                .enter()
                .append('g')
                .attr('class', 'fecal');

            type2.selectAll('dot')
                .data(function (d) {
                    return d.values.map(function (e) {
                        e['name'] = d.name;
                        e['key'] = 'fecal_coliform';
                        e['site'] = window.site2Id;
                        return e;
                    });
                })
                .enter().append('path')
                .attr('transform', function (d) {
                    return 'translate(' + x(new Date(d.date)) + ', ' +
                            y(d.value) + ')';
                })
                .attr('d', d3.symbol())
                .style('stroke', '#000000')
                .style('fill', '#000000')
                .style('cursor', 'pointer')
                .on('mouseover', showMouseover);
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

/*******************************************************************************
 *******************************************************************************
 *
 * Manager
 *
 *******************************************************************************
 ******************************************************************************/

$(function () {
    $('input[type=date]').val('');

    $('div.graph').on('click mouseleave', function() {
        $(this).find('.popup').remove();
    });
    $('#remove_site').on('click', function() {
        window.hasSiteTwo = false;
        window.data.site2 = null;
        window.site2Id = null;
        filtered2 = {};
        $('#site-names').hide();
        $(this).addClass('disabled');
        $('div.graph').removeClass("l6").addClass("l10 offset-l1");
        $('div.graph').css("width", "");
        centerHover();
        createGraph();
    });
    $('div.date select').change(function() {
        var parent = $(this).parent().parent().parent();
        var input = parent.find('input.date');
        var year = parent.find('select.year').toArray()[0].value;
        var month = parent.find('select.month').toArray()[0].value;
        var day = parent.find('select.day').toArray()[0].value;
        if (month && parseInt(month) < 10) {
            month = "0" + month;
        }
        if (day && parseInt(day) < 10) {
            day = "0" + day;
        }
        if (year && month && day) {
            var str = year + "-" + month + "-" + day;
            input.val(str);
            changeRangeStart();
            changeRangeEnd();
        }
    });
    centerHover();
    createGraph();
});

$(window).click(function(){
  if($('div.search-results')){
    $('div.search-results').hide();
  }
});

$(window).resize(function () {
    if (window.hasSiteTwo) {
        $('div.graph').css("width", "50%");
    }
    centerHover();
    createGraph();
});

var centerHover = function centerHover() {
    $('div.graph:visible div.data-info, div#water-parameter-pdf').each(function(i, e) {
        var width = $(e).width();
        var parentWidth = $(e).parent().width();
        $(e).css("left", (parentWidth - width)/2 + "px");
    })
}

var loadSite2 = function loadSite2(site_slug) {
    $.getJSON('/sites/'+site_slug+'/water/data/', function(data) {
        window.hasSiteTwo = true;
        window.data.site2 = data.data;
        window.site2Id = data.site.site_slug;
        $('#site2-header').text(data.site.site_name);
        $('#site-names').show();
        $('#remove_site').removeClass("disabled");
        $("div.graph").removeClass("l10 offset-l1").addClass("l6")
            .css("width", "50%");
        centerHover();
        createGraph();
        $('div.search-results').hide();
        $('input#search').val('');
    })
}

var graphFunc = {
    'temperature': graphTemperature,
    'oxygen': graphOxygen,
    'ph': graphPH,
    'turbidity': graphTurbidity,
    'salinity': graphSalinity,
    'conductivity': graphConductivity,
    'dissolved': graphDissolved,
    'bod': graphBod,
    'coliform': graphColiform
};

var toggleGraph = function toggleGraph(name) {

    fadeOutGraph(name);

    var checkInput = $('input').toArray().filter(function(input) {
        return input.type == 'checkbox' && input.checked;
    });

    fadeInGraph(name);
};

var fadeInGraph = function fadeInGraph(name) {
    if ($('#' + name + '-control').prop('checked')) {
        $('#graph-site1-' + name).fadeIn();
        if (window.hasSiteTwo) {
            $('#graph-site2-' + name).fadeIn();
        }
    }
}

var fadeOutGraph = function fadeOutGraph(name) {
    if (!$('#' + name + '-control').prop('checked')){
        $('#graph-site1-' + name).fadeOut();
        if (window.hasSiteTwo) {
            $('#graph-site2-' + name).fadeOut();
        }
    }
}

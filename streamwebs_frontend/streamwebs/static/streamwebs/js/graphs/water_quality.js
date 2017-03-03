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

    for (let datum of data) {
        const date = parseInt(datum.date, 10) * 1000; // Convert from seconds to millis
        if (date >= date_range[1] || date <= date_range[0]) {
            continue;
        }

        datum.date = new Date(date);

        formatted.push(datum);
    }

    formatted.sort((a, b) => {
        return a.date - b.date;
    });

    const types = {
        /*
         * So we currently have a list of data points, each one containing a date
         * and a list of 4 samples, each sample having one each of every data type
         * we need. Instead, we want to pull out just one type per data point and
         * pair it with the date.
         *
         * Get comfortable with this code, because we're about to repeat it for
         * every data type.
         */
        water_temperature: formatted.map((d) => {
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
                    return ((prev * idx) + parseFloat(curr.water_temperature)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        air_temperature: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.air_temperature)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        dissolved_oxygen: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.dissolved_oxygen)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        pH: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.pH)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        turbidity: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.turbidity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        salinity: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.salinity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        conductivity: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.conductivity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        fecal_coliform: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.fecal_coliform)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        total_solids: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.total_solids)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        bod: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.bod)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        ammonia: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.ammonia)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        nitrite: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrite)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        nitrate: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrate)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        phosphates: formatted.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.phosphates)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
    };

    const margin = {top: 20, right: 100, bottom: 30, left: 40};
    const defineWidth = function definedefineWidth(container) {
        return container.width() - (margin.right + margin.left);
    };

    const defineHeight = function definedefineHeight(container) {
        return 300 - (margin.top + margin.bottom);
    };

    /***************************************************************************
     * Temperature
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-temperature';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const water_min = d3.min(types.water_temperature, d => {
            // Sometimes we have NaN, null, or undefined, so remove those
            // so that d3.min returns a numeric value
            return d.value || 0;
        }) || 0; // If d3.min is given an empty array, it returns Nan,
                 // So substitute a reasonable default
        const air_min = d3.min(types.air_temperature, d => {
            return d.value || 0;
        }) || 0;
        const water_max = d3.max(types.water_temperature, (d) => {
            return d.value || 1;
        }) || 1;
        const air_max = d3.max(types.air_temperature, (d) => {
            return d.value || 1;
        }) || 1;
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(0, water_min, air_min)) || 0,
                Math.ceil(Math.max(1, water_max, air_max)) || 1
            ])
            .range([height, 0]);
        const z = d3.scaleOrdinal()
            .domain(['Air Temperature', 'Water Temperature'])
            .range(['#6cbcfc', '#0310fc']);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.water_temperature.length > 0 || types.air_temperature.length > 0) {
            const type = g.selectAll('.temp')
                .data([
                    {
                        name: "Water Temperature",
                        values: types.water_temperature
                    },
                    {name: "Air Temperature", values: types.air_temperature},
                ])
                .enter()
                .append('g')
                .attr('class', 'temp');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', (d) => {
                    return z(d.name)
                });

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
                .data([
                    {
                        name: "Water Temperature",
                        values: types.water_temperature
                    },
                    {name: "Air Temperature", values: types.air_temperature},
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
        } else {
            $('#temperature-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Dissolved Oxygen
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-oxygen';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([0, Math.ceil(d3.max(types.dissolved_oxygen, (d) => {
                return d.value || 1;
            }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.dissolved_oxygen.length > 0) {
            const type = g.selectAll('.do')
                .data([{
                    name: 'Dissolved Oxygen',
                    values: types.dissolved_oxygen
                }])
                .enter()
                .append('g')
                .attr('class', 'do');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#93ece9');

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
                .style('stroke', '#93ece9')
                .style('fill', '#93ece9');
        } else {
            $('#oxygen-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * pH
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-ph';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([0, 14])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.pH.length > 0) {
            const type = g.selectAll('.ph')
                .data([{name: 'pH', values: types.pH}])
                .enter()
                .append('g')
                .attr('class', 'ph');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#aede5b');

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
                .style('stroke', '#aede5b')
                .style('fill', '#aede5b');
        } else {
            $('#ph-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Turbidity
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-turbidity';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(0, d3.min(types.turbidity, (d) => {
                    return d.value || 0;
                }) || 0)),
                Math.ceil(d3.max(types.turbidity, (d) => {
                    return d.value || 1;
                }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.turbidity.length > 0) {
            const type = g.selectAll('.turb')
                .data([{name: 'Turbidity', values: types.turbidity}])
                .enter()
                .append('g')
                .attr('class', 'turb');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#636363');

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
                .style('stroke', '#636363')
                .style('fill', '#636363');
        } else {
            $('#turbidity-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Salinity
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-salinity';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(0, d3.min(types.salinity, (d) => {
                    return d.value || 0;
                }) || 0)),
                Math.ceil(d3.max(types.salinity, (d) => {
                    return d.value || 1;
                }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.salinity.length > 0) {
            const type = g.selectAll('.sal')
                .data([{name: 'Salinity', values: types.salinity}])
                .enter()
                .append('g')
                .attr('class', 'sal');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#cccccc');

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
                .style('stroke', '#cccccc')
                .style('fill', '#cccccc');
        } else {
            $('#salinity-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Conductivity
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-conductivity';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([0,
                Math.ceil(d3.max(types.conductivity, (d) => {
                    return d.value || 1;
                }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.conductivity.length > 0) {
            const type = g.selectAll('.cond')
                .data([{name: 'Conductivity', values: types.conductivity}])
                .enter()
                .append('g')
                .attr('class', 'cond');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#f7f73e');

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
                .style('stroke', '#f7f73e')
                .style('fill', '#f7f73e');
        } else {
            $('#conductivity-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Dissolved Solids
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-dissolved';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types.total_solids, (d) => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types.ammonia, (d) => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types.nitrate, (d) => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types.nitrite, (d) => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types.phosphates, (d) => {
                        return d.value || 0;
                    }) || 0
                )),
                Math.ceil(
                    d3.max(types.total_solids, (d) => {
                        return d.value || 1;
                    }) || 1
                )
            ])
            .range([height, 0]);

        const z = d3.scaleOrdinal()
            .domain(['Total Solids', 'Ammonia', 'Nitrite', 'Nitrate', 'Phosphates'])
            .range(['#ababab', '#bfbf30', '#a8bf13', '#c8e60b', '#c9833c']);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.total_solids.length > 0) {
            const type = g.selectAll('.solids')
                .data([
                    {name: "Total Solids", values: types.total_solids},
                    {name: "Ammonia", values: types.ammonia},
                    {name: "Nitrite", values: types.nitrite},
                    {name: "Nitrate", values: types.nitrate},
                    {name: "Phosphates", values: types.phosphates},
                ])
                .enter()
                .append('g')
                .attr('class', 'solids');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', (d) => {
                    return z(d.name)
                });

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
                .data([
                    {name: "Total Solids", values: types.total_solids},
                    {name: "Ammonia", values: types.ammonia},
                    {name: "Nitrite", values: types.nitrite},
                    {name: "Nitrate", values: types.nitrate},
                    {name: "Phosphates", values: types.phosphates},
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
        } else {
            $('#dissolved-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * BOD
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-bod';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([0,
                Math.ceil(d3.max(types.bod, (d) => {
                    return d.value || 1;
                }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.bod.length > 0) {
            const type = g.selectAll('.bod')
                .data([{name: 'BOD', values: types.bod}])
                .enter()
                .append('g')
                .attr('class', 'bod');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#6851ed');

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
                .style('stroke', '#6851ed')
                .style('fill', '#6851ed');
        } else {
            $('#bod-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }

    /***************************************************************************
     * Fecal Coliform
     **************************************************************************/

    {
        const containerName = '#graph-' + siteId + '-coliform';
        const container = outerContainer.find(containerName);
        const width = defineWidth(container);
        const height = defineHeight(container);

        const x = d3.scaleTime()
            .range([0, width]);
        x.domain([
            date_range[0] !== 0 ? new Date(date_range[0]) :
                d3.min(formatted, (d) => {
                    return new Date(d.date)
                }),
            date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                d3.max(formatted, (d) => {
                    return new Date(d.date)
                }),
        ]);
        const y = d3.scaleLinear()
            .domain([0,
                Math.ceil(d3.max(types.fecal_coliform, (d) => {
                    return d.value || 1;
                }) || 1)
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x((d) => {
                return x(d.date)
            })
            .y((d) => {
                return y(d.value)
            });

        const svg = d3.select(containerName).append('svg')
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

        if (types.fecal_coliform.length > 0) {
            const type = g.selectAll('.fecal')
                .data([{name: 'Fecal Coliform', values: types.fecal_coliform}])
                .enter()
                .append('g')
                .attr('class', 'fecal');

            type.append('path')
                .attr('class', 'line')
                .attr('d', (d) => {
                    return line(d.values)
                })
                .style('stroke', '#593e29');

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
                .style('stroke', '#593e29')
                .style('fill', '#593e29');
        } else {
            $('#coliform-control').attr('disabled', 'disabled');
            container.css({display: 'none'});
        }
    }
};

$(() => {
    $('input[type=date]').val('');
    $('#date-start').change(changeRangeStart);
    $('#date-end').change(changeRangeEnd);

    createGraph();
});

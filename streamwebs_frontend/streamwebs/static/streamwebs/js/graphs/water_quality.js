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

    const types1 = {
        /*
         * So we currently have a list of data points, each one containing a date
         * and a list of 4 samples, each sample having one each of every data type
         * we need. Instead, we want to pull out just one type per data point and
         * pair it with the date.
         *
         * Get comfortable with this code, because we're about to repeat it for
         * every data type.
         */
        water_temperature: formatted1.map((d) => {
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
        air_temperature: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.air_temperature)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        dissolved_oxygen: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.dissolved_oxygen)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        pH: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.pH)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        turbidity: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.turbidity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        salinity: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.salinity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        conductivity: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.conductivity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        fecal_coliform: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.fecal_coliform)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        total_solids: formatted1.map((d) => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.total_solids)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        bod: formatted1.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.bod)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        ammonia: formatted1.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.ammonia)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        nitrite: formatted1.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrite)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        nitrate: formatted1.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrate)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        }),
        phosphates: formatted1.map(d => {
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

    const formatted2 = [];
    const types2 = {};

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

        types2.water_temperature = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.water_temperature)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.air_temperature = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.air_temperature)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.dissolved_oxygen = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.dissolved_oxygen)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.pH = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.pH)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.turbidity = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.turbidity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.salinity = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.salinity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.conductivity = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.conductivity)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.fecal_coliform = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.fecal_coliform)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.total_solids = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.total_solids)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.bod = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.bod)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.ammonia = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.ammonia)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.nitrite = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrite)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.nitrate = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.nitrate)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
        types2.phosphates = formatted2.map(d => {
            return {
                date: d.date,
                value: d.samples.reduce((prev, curr, idx) => {
                    return ((prev * idx) + parseFloat(curr.phosphates)) / (idx + 1);
                }, 0),
            };
        }).filter(d => {
            return !isNaN(d.value);
        });
    }

    const margin = {top: 20, right: 150, bottom: 30, left: 40};
    const defineWidth = function definedefineWidth(container) {
        return container.width() - (margin.right + margin.left);
    };

    const defineHeight = function definedefineHeight() {
        return 300 - (margin.top + margin.bottom);
    };

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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                ),
            ]);
        const min = Math.min(
            0,
            d3.min(types1.water_temperature, d => {
                return d.value || 0;
            }) || 0,
            d3.min(types1.air_temperature, d => {
                return d.value || 0;
            }) || 0,
            window.hasSiteTwo ? d3.min(types2.water_temperature, d => {
                return d.value || 0;
            }) || 0 : 0,
            window.hasSiteTwo ? d3.min(types2.air_temperature, d => {
                return d.value || 0;
            }) || 0 : 0
        );
        const max = Math.max(
            1,
            d3.max(types1.water_temperature, d => {
                return d.value || 1;
            }) || 1,
            d3.max(types1.air_temperature, d => {
                return d.value || 1;
            }) || 1,
            window.hasSiteTwo ? d3.max(types2.water_temperature, d => {
                return d.value || 1;
            }) || 1 : 0,
            window.hasSiteTwo ? d3.max(types2.air_temperature, d => {
                return d.value || 1;
            }) || 1 : 0
        );
        const y = d3.scaleLinear()
            .domain([
                Math.floor(min) || 0,
                Math.ceil(max) || 1
            ])
            .range([height, 0]);
        const z = d3.scaleOrdinal()
            .domain(['Air Temperature', 'Water Temperature'])
            .range(['#6cbcfc', '#0310fc']);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', d => {
                        return z(d.name)
                    });

                type1.selectAll('dot')
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
                    });

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

                legend1.append('rect')
                    .attr('x', 2)
                    .attr('width', 18)
                    .attr('height', 2)
                    .attr('fill', d => {
                        return z(d.name);
                    });

                legend1.append('text')
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', d => {
                        return z(d.name)
                    });

                type2.selectAll('dot')
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
                    });

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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                ),
            ]);
        const y = d3.scaleLinear()
            .domain([0, Math.ceil(Math.max(
                d3.max(types1.dissolved_oxygen, d => {
                    return d.value || 1;
                }) || 1,
                window.hasSiteTwo ? d3.max(types2.dissolved_oxygen, d => {
                    return d.value || 1;
                }) || 1 : Number.MIN_SAFE_INTEGER)) || 1
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#93ece9');

                type1.selectAll('dot')
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
                    .style('stroke', '#93ece9')
                    .style('fill', '#93ece9');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#93ece9');

                type2.selectAll('dot')
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
                    .style('stroke', '#93ece9')
                    .style('fill', '#93ece9');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                ),
        ]);
        const y = d3.scaleLinear()
            .domain([0, 14])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#aede5b');

                type1.selectAll('dot')
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
                    .style('stroke', '#aede5b')
                    .style('fill', '#aede5b');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#aede5b');

                type2.selectAll('dot')
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
                    .style('stroke', '#aede5b')
                    .style('fill', '#aede5b');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                ),
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.turbidity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.turbidity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    0,
                    d3.max(types1.turbidity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.max(types2.turbidity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MIN_SAFE_INTEGER
                )),
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#636363');

                type1.selectAll('dot')
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
                    .style('stroke', '#636363')
                    .style('fill', '#636363');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#636363');

                type2.selectAll('dot')
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
                    .style('stroke', '#636363')
                    .style('fill', '#636363');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                )
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.salinity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.salinity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    0,
                    d3.max(types1.salinity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.max(types2.salinity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MIN_SAFE_INTEGER
                )),
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#cccccc');

                type1.selectAll('dot')
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
                    .style('stroke', '#cccccc')
                    .style('fill', '#cccccc');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#cccccc');

                type2.selectAll('dot')
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
                    .style('stroke', '#cccccc')
                    .style('fill', '#cccccc');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                )
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.conductivity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.conductivity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    0,
                    d3.max(types1.conductivity, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.max(types2.conductivity, d => {
                        return d.value || 0;
                    }) || 0 : Number.MIN_SAFE_INTEGER
                )),
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#f7f73e');

                type1.selectAll('dot')
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
                    .style('stroke', '#f7f73e')
                    .style('fill', '#f7f73e');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#f7f73e');

                type2.selectAll('dot')
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
                    .style('stroke', '#f7f73e')
                    .style('fill', '#f7f73e');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                )
            ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.total_solids, d => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types1.ammonia, d => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types1.nitrate, d => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types1.nitrite, d => {
                        return d.value || 0;
                    }) || 0,
                    d3.min(types1.phosphates, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.total_solids, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.min(types2.ammonia, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.min(types2.nitrate, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.min(types2.nitrite, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.min(types2.phosphates, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    d3.max(types1.total_solids, d => {
                        return d.value || 1;
                    }) || 1,
                    d3.max(types1.ammonia, d => {
                        return d.value || 1;
                    }) || 1,
                    d3.max(types1.nitrate, d => {
                        return d.value || 1;
                    }) || 1,
                    d3.max(types1.nitrite, d => {
                        return d.value || 1;
                    }) || 1,
                    d3.max(types1.phosphates, d => {
                        return d.value || 1;
                    }) || 1,
                    window.hasSiteTwo ? d3.max(types2.total_solids, d => {
                        return d.value || 1;
                    }) || 1 : Number.MIN_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.max(types2.ammonia, d => {
                        return d.value || 1;
                    }) || 1 : Number.MIN_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.max(types2.nitrate, d => {
                        return d.value || 1;
                    }) || 1 : Number.MIN_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.max(types2.nitrite, d => {
                        return d.value || 1;
                    }) || 1 : Number.MIN_SAFE_INTEGER,
                    window.hasSiteTwo ? d3.max(types2.phosphates, d => {
                        return d.value || 1;
                    }) || 1 : Number.MIN_SAFE_INTEGER
                ))
            ])
            .range([height, 0]);

        const z = d3.scaleOrdinal()
            .domain(['Total Solids', 'Ammonia', 'Nitrite', 'Nitrate', 'Phosphates'])
            .range(['#ababab', '#bfbf30', '#a8bf13', '#c8e60b', '#c9833c']);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', d => {
                        return z(d.name)
                    });

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
                    });

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

                type.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', d => {
                        return z(d.name)
                    });

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
                    });

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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                )
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.bod, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.bod, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    0,
                    d3.max(types1.bod, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.max(types2.bod, d => {
                        return d.value || 0;
                    }) || 0 : Number.MIN_SAFE_INTEGER
                )),
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#6851ed');

                type1.selectAll('dot')
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
                    .style('stroke', '#6851ed')
                    .style('fill', '#6851ed');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#6851ed');

                type2.selectAll('dot')
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
                    .style('stroke', '#6851ed')
                    .style('fill', '#6851ed');
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
            .domain([
                date_range[0] !== Number.MIN_SAFE_INTEGER ? new Date(date_range[0]) :
                Math.min(
                    d3.min(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.min(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MAX_SAFE_INTEGER
                ),
                date_range[1] !== Number.MAX_SAFE_INTEGER ? new Date(date_range[1]) :
                Math.max(
                    d3.max(formatted1, d => {
                        return new Date(d.date)
                    }),
                    window.hasSiteTwo ? d3.max(formatted2, d => {
                        return new Date(d.date)
                    }) : Number.MIN_SAFE_INTEGER
                )
        ]);
        const y = d3.scaleLinear()
            .domain([
                Math.floor(Math.min(
                    0,
                    d3.min(types1.fecal_coliform, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.min(types2.fecal_coliform, d => {
                        return d.value || 0;
                    }) || 0 : Number.MAX_SAFE_INTEGER
                )),
                Math.ceil(Math.max(
                    0,
                    d3.max(types1.fecal_coliform, d => {
                        return d.value || 0;
                    }) || 0,
                    window.hasSiteTwo ? d3.max(types2.fecal_coliform, d => {
                        return d.value || 0;
                    }) || 0 : Number.MIN_SAFE_INTEGER
                )),
            ])
            .range([height, 0]);

        const line = d3.line()
            .curve(d3.curveLinear)
            .x(d => {
                return x(d.date)
            })
            .y(d => {
                return y(d.value)
            });

        const svg1 = d3.select(containerName1).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g1 = svg1.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g1.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g1.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

        const svg2 = d3.select(containerName2).append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const g2 = svg2.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

        g2.append('g')
            .attr('class', 'axis axis--x')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(d3.axisBottom(x));

        g2.append('g')
            .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));

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

                type1.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#593e29');

                type1.selectAll('dot')
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
                    .style('stroke', '#593e29')
                    .style('fill', '#593e29');
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

                type2.append('path')
                    .attr('class', 'line')
                    .attr('d', d => {
                        return line(d.values)
                    })
                    .style('stroke', '#593e29');

                type2.selectAll('dot')
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
                    .style('stroke', '#593e29')
                    .style('fill', '#593e29');
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
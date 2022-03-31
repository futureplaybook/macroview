var dataPathHSI = '/macroview/data/data_HSI.json'
var containerHSI = 'containerHSI'
Highcharts.getJSON(dataPathHSI, function(data) {
    Highcharts.stockChart(containerHSI, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'HSI Index'
        },

        subtitle: {
            text: 'More details here'
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            }
        },

        legend: {
            enabled: true
        },
        credits: {
            enabled: false
        },
        scrollbar: {
            enabled: false
        },
        exporting: {
            enabled: false
        },

        series: [{
                name: 'HSi Index',
                data: data,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
            {
                type: 'flags',
                showInLegend: false,
                data: [{
                    x: Date.UTC(2010, 11, 1),
                    title: 'A',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2015, 11, 12),
                    title: 'B',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2017, 11, 22),
                    title: 'C',
                    text: 'Some event with a description'
                }],
                onSeries: 'dataseries',
                shape: 'squarepin',
                width: 16
            }
        ]
    });
});









var dataPathJPY = '/macroview/data/data_JPY.json'
var containerJPY = 'containerJPY'
Highcharts.getJSON(dataPathJPY, function(data) {
    Highcharts.stockChart(containerJPY, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Yen'
        },

        subtitle: {
            text: 'More details here'
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            }
        },

        legend: {
            enabled: true
        },
        credits: {
            enabled: false
        },

        rangeSelector: {
            enabled: false
        },

        navigator: {
            enabled: false
        },
        scrollbar: {
            enabled: false
        },
        exporting: {
            enabled: false
        },

        series: [{
                name: 'Yen',
                data: data,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
            {
                type: 'flags',
                showInLegend: false,
                data: [{
                    x: Date.UTC(2010, 11, 1),
                    title: 'A',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2015, 11, 12),
                    title: 'B',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2017, 11, 22),
                    title: 'C',
                    text: 'Some event with a description'
                }],
                onSeries: 'dataseries',
                shape: 'squarepin',
                width: 16
            }
        ]
    });
});



var dataPathShillerPE = '/macroview/data/data_MULTPL_SHILLER_PE_RATIO_MONTH.json'
var containerShillerPE = 'containerShillerPE'
Highcharts.getJSON(dataPathShillerPE, function(data) {
    Highcharts.stockChart(containerShillerPE, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Shiller PE'
        },

        subtitle: {
            text: 'More details here'
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            }
        },

        legend: {
            enabled: true
        },
        credits: {
            enabled: false
        },

        rangeSelector: {
            enabled: false
        },

        navigator: {
            enabled: false
        },
        scrollbar: {
            enabled: false
        },
        exporting: {
            enabled: false
        },

        series: [{
                name: 'Shiller PE',
                data: data,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
            {
                type: 'flags',
                showInLegend: false,
                data: [{
                    x: Date.UTC(2010, 11, 1),
                    title: 'A',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2015, 11, 12),
                    title: 'B',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2017, 11, 22),
                    title: 'C',
                    text: 'Some event with a description'
                }],
                onSeries: 'dataseries',
                shape: 'squarepin',
                width: 16
            }
        ]
    });
});






var dataPathCoreCPI = '/macroview/data/data_coreCPIYOY.json'
var containerCoreCPI = 'containerCoreCPI'
Highcharts.getJSON(dataPathCoreCPI, function(data) {
    Highcharts.stockChart(containerCoreCPI, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Core CPI'
        },

        subtitle: {
            text: 'More details here'
        },

        xAxis: {
            scrollbar: {
                enabled: false,
            },
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            }
        },

        legend: {
            enabled: true
        },
        credits: {
            enabled: false
        },

        rangeSelector: {
            enabled: false
        },

        navigator: {
            enabled: false
        },
        scrollbar: {
            enabled: false
        },
        exporting: {
            enabled: false
        },

        series: [{
                name: 'Core CPI',
                data: data,
                id: 'dataseries',
                tooltip: {
                    valueDecimals: 2
                }
            },
            {
                type: 'flags',
                showInLegend: false,
                data: [{
                    x: Date.UTC(2010, 11, 1),
                    title: 'A',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2015, 11, 12),
                    title: 'B',
                    text: 'Some event with a description'
                }, {
                    x: Date.UTC(2017, 11, 22),
                    title: 'C',
                    text: 'Some event with a description'
                }],
                onSeries: 'dataseries',
                shape: 'squarepin',
                width: 16
            }
        ]
    });
});
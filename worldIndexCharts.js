var dataPathGSPC = '/macroview/data/data_GSPC.json'
var containerGSPC = 'containerGSPC'
Highcharts.getJSON(dataPathGSPC, function(data) {
    Highcharts.stockChart(containerGSPC, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'SP 500'
        },

        subtitle: {
            text: 'More details here'
        },

        xAxis: {
            scrollbar: {
                enabled: false,
            },
            width: '95%'
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            },
            width: '100%'
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
                name: 'SP 500',
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






var dataPathIXIC = '/macroview/data/data_IXIC.json'
var containerIXIC = 'containerIXIC'
Highcharts.getJSON(dataPathIXIC, function(data) {
    Highcharts.stockChart(containerIXIC, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Nasdaq'
        },

        subtitle: {
            text: 'More details here'
        },

        xAxis: {
            scrollbar: {
                enabled: false,
            },
            width: '95%'
        },

        yAxis: {
            title: {
                text: 'Exchange rate'
            },
            width: '100%'
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
                name: 'Nasdaq',
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
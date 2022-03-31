var dataPathGold = '/macroview/data/data_GC.json'
var containerGold = 'containerGold'
Highcharts.getJSON(dataPathGold, function(data) {
    Highcharts.stockChart(containerGold, {
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
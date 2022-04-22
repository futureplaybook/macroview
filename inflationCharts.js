var dataPathDGS10 = '/macroview/data/data_DGS10.json'
var containerDGS10 = 'containerDGS10'
Highcharts.getJSON(dataPathDGS10, function(data) {
    Highcharts.stockChart(containerDGS10, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'US Nominal Yield'
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
            name: 'US Nominal Yield',
            data: data,
            id: 'dataseries',
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});




var dataPathDFII10 = '/macroview/data/data_DFII10.json'
var containerDFII10 = 'containerDFII10'
Highcharts.getJSON(dataPathDFII10, function(data) {
    Highcharts.stockChart(containerDFII10, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'US Real Yield'
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
            name: 'US Real Yield',
            data: data,
            id: 'dataseries',
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});
var dataPathGold = '/macroview/data/data_GC.json'
var containerGold = 'containerGold'
Highcharts.getJSON(dataPathGold, function(data) {
    Highcharts.stockChart(containerGold, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Gold'
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
            name: 'Gold',
            data: data,
            id: 'dataseries',
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});






var dataPathCrude = '/macroview/data/data_CL.json'
var containerCrude = 'containerCrude'
Highcharts.getJSON(dataPathCrude, function(data) {
    Highcharts.stockChart(containerCrude, {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Crude'
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
            name: 'Crude',
            data: data,
            id: 'dataseries',
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});
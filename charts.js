// https://demo-live-data.highcharts.com/aapl-historical.json
// https://futureplaybook.github.io/demoHTML/data_SHILLER_PE_RATIO_MONTH.json
// 'data_SHILLER_PE_RATIO_MONTH.json'
// 'data_MULTPL_SHILLER_PE_RATIO_MONTH.json'
Highcharts.getJSON(meta['dataFilename'], function(data) {
    Highcharts.stockChart('container', {
        rangeSelector: {
            selected: 5
        },

        title: {
            text: meta["displayName"]
        },

        subtitle: {
            text: 'Data ranged from ' + meta['dataFrom'] + ' - ' + meta['dataTo']
        },

        xAxis: {
            width: '95%'
        },

        yAxis: {
            title: {
                text: ''
            },
            width: '100%'
        },
        scrollbar: {
            enabled: false
        },

        legend: {
            enabled: true
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },

        series: [{
            name: meta["displayName"],
            data: data,
            id: 'dataseries',
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});
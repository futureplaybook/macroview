
            var seriesOptions = [],
                seriesCounter = 0,
                //names = ['USA', 'EUR', 'GBR','JPN'];
                names = ['XLF', 'XLK'];
            /**
             * Create the chart when all data is loaded
             * @returns {undefined}
             */
            function createChart() {

                Highcharts.stockChart('container', {

                    rangeSelector: {
                        selected: 4
                    },

                    yAxis: {
                        labels: {
                            formatter: function () {
                                return (this.value > 0 ? ' + ' : '') + this.value + '%';
                            }
                        },
                        plotLines: [{
                            value: 0,
                            width: 2,
                            color: 'silver'
                        }]
                    },

                    plotOptions: {
                        series: {
                            compare: 'value',
                            compareStart: true,
                            showInNavigator: true
                        }
                    },

                    legend: {
                        enabled: true
                    },
                    
                    exporting: {
                        enabled: false
                    },
                    scrollbar: {
                        enabled: false
                    },


                    tooltip: {
                        pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                        valueDecimals: 2,
                        split: true
                    },

                    series: seriesOptions
                });
            }

            function success(data) {
                //var name = this.url.match(/(USA|EUR|GBR|JPN)/)[0].toUpperCase();
                //var name = this.url.match(/(USA|EUR|GBR|JPN)/)[0]
                var name = this.url.match(/(XLF|XLK)/)[0]
                var i = names.indexOf(name);
                seriesOptions[i] = {
                    name: name,
                    data: data,
                    id:  name
                };
                console.log(name)

                // As we're loading the data asynchronously, we don't know what order it
                // will arrive. So we keep a counter and create the chart when all the data is loaded.
                seriesCounter += 1;

                if (seriesCounter === names.length) {
                    createChart();
                }
            }

            // Highcharts.getJSON(
            //     'http://127.0.0.1:8887/macroview/data/data_RATEINF_INFLATION_USA.json',
            //     success
            // );
            // Highcharts.getJSON(
            //     'http://127.0.0.1:8887/macroview/data/data_RATEINF_INFLATION_EUR.json',
            //     success
            // );
            // Highcharts.getJSON(
            //     'http://127.0.0.1:8887/macroview/data/data_RATEINF_INFLATION_GBR.json',
            //     success
            // );
            // Highcharts.getJSON(
            //     'http://127.0.0.1:8887/macroview/data/data_RATEINF_INFLATION_JPN.json',
            //     success
            // );

            Highcharts.getJSON(
                'http://127.0.0.1:8887/macroview/data/data_XLF.json',
                success
            );
            Highcharts.getJSON(
                'http://127.0.0.1:8887/macroview/data/data_XLK.json',
                success
            );



    
import Vue from 'vue';
import * as d3 from 'd3';
const moment = require('moment');

const uniqueColors = [
    '#e6194B',
    '#3cb44b',
    '#ffe119',
    '#4363d8',
    '#f58231',
    '#911eb4',
    '#42d4f4',
    '#f032e6',
    '#bfef45',
    '#fabebe',
    '#469990',
    '#e6beff',
    '#9A6324',
    '#fffac8',
    '#800000',
    '#aaffc3',
    '#808000',
    '#ffd8b1',
    '#000075',
    '#a9a9a9',
    '#ffffff',
    '#000000'
];

Vue.component('stock-plot', {
    props: ['plotHeight', 'plotWidth'],
    data: function() {
        return {
            plotMargin : {
                top: 5,
                bottom: 5,
                left: 10,
                right: 10 
            }
        }
    },
    methods: {
        recreateAllGraphs: function() {
            let fullPlotArea = d3.select('#fullPlot');
            let plotSvg = fullPlotArea.select('svg');
            let timeParser = d3.timeParse('%m %d %Y');
            function parseTimeForD3(d) {
                // Parse using the more flexible moments library.
                let parsedData = moment(d.dateTime);
                
                // Reformat string to feed into d3 timeParse.
                let reformattedString = parsedData.format('MM DD YYYY');
                return timeParser(reformattedString);
            }

            let xAxis = d3.scaleTime()
                .domain([this.$store.state.minDate, this.$store.state.maxDate])
                .range([0, 1000]);
            let yAxis = d3.scaleLinear()
                .domain([0.0, this.$store.state.maxPrice])
                .range([1000, 0]);

            let stockPriceLinePlot = d3.line()
                .x(function(d) {
                    return xAxis(parseTimeForD3(d)); 
                })
                .y(function(d) { return yAxis(d.closePrice); });

            let lineGraphs = plotSvg
                .selectAll('path') 
                .data(this.$store.state.stocks);
            lineGraphs
                .enter().append('path');
            lineGraphs.exit().remove();
            lineGraphs
                .datum(function(d) { return d.priceInfo; })
                .attr('fill', 'none')
                .attr('stroke', function(d, i) {
                    return uniqueColors[i % uniqueColors.length];
                })
                .attr('stroke-width', 1.5)
                .attr('d', stockPriceLinePlot);
        }
    },
    computed: {
        clientPlotHeight: function() {
            return this.plotHeight - this.$data.plotMargin.top - this.$data.plotMargin.bottom;
        },
        clientPlotWidth: function() {
            return this.plotWidth - this.$data.plotMargin.left - this.$data.plotMargin.right;
        }
    },
    mounted: function() {
        // This watches when the total list of stocks changes (to know which stocks are
        // are not relevant.
        this.$store.watch(
            (state, getters) => {
                return state.stocks;
            },
            (newValue, oldValue) => {
                this.recreateAllGraphs();
            }
        );

        // This watches whenever we receive price information to update the chart so we
        // can know when to refresh the chart.
        this.$store.subscribe((mutation, state) => {
            if (mutation.type != 'setPriceInfo') {
                return;
            }
            this.recreateAllGraphs();
        });
    },
    template: `
        <section>
            <div id="rangeControl">

            </div>
            <div id="fullPlot">
                <svg v-bind:width="clientPlotWidth" 
                     v-bind:height="clientPlotHeight"
                     viewBox="0 0 1000 1000"
                     preserveAspectRatio="none"
                     v-bind:transform="'translate(' + plotMargin.left + ',' + plotMargin.top + ')'">
                </svg>
            </div>
        </section>
    `
});

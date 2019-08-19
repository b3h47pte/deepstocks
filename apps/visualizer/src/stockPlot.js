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
                left: 5,
                right: 5 
            },
            xAxisY: 0
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

            // Go from just below min price to just above max price
            let useMinPrice = this.$store.state.minPrice;
            let useMaxPrice = this.$store.state.maxPrice;
            const delta = useMaxPrice - useMinPrice;
            useMinPrice -= delta * 0.01;
            useMaxPrice += delta * 0.01;

            let xAxisScale = d3.scaleTime()
                .range([0, 1000])
                .domain([this.$store.state.minDate, this.$store.state.maxDate]);
            let yAxisScale = d3.scaleLinear()
                .range([980, 20]) // Don't use full range to leave some space at the bottom for the x-axis.
                .domain([useMinPrice, useMaxPrice])
                .nice();

            // Draw closing price plot.
            let stockPriceLinePlot = d3.line()
                .x(function(d) {
                    return xAxisScale(parseTimeForD3(d)); 
                })
                .y(function(d) { return yAxisScale(d.closePrice); });

            let lineGraphs = plotSvg
                .selectAll('path.CLASS_FOR_ID_PLOT') 
                .data(this.$store.state.stocks);
            lineGraphs
                .enter()
                .append('path')
                .attr('class', 'CLASS_FOR_ID_PLOT');
            lineGraphs.exit().remove();
            lineGraphs
                .datum(function(d) { return d.priceInfo; })
                .attr('fill', 'none')
                .attr('stroke', function(d, i) {
                    return uniqueColors[i % uniqueColors.length];
                })
                .attr('stroke-width', 1.5)
                .attr('d', stockPriceLinePlot);

            // Draw axes.
            let xAxis = d3.axisBottom(xAxisScale);
            let yAxis = d3.axisLeft(yAxisScale);

            plotSvg
                .select('#xAxis')
                .call(xAxis);
            plotSvg
                .select('#yAxis')
                .call(yAxis);

            // Find first tick of the Y-axis to figure out where the min-point is so we know where to
            // stick the x-axis.
            const zeroTick = plotSvg.select('#yAxis g.tick');
            const zeroTickXform = zeroTick.attr('transform');
            const translationRegex = /translate\((.*),(.*)\)/g;
            const parsedXform = translationRegex.exec(zeroTickXform);
            this.$data.xAxisY = parseFloat(parsedXform[2]);
        }
    },
    computed: {
        clientPlotHeight: function() {
            return this.plotHeight - this.$data.plotMargin.top - this.$data.plotMargin.bottom;
        },
        clientPlotWidth: function() {
            return this.plotWidth - this.$data.plotMargin.left - this.$data.plotMargin.right;
        },
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
                     preserveAspectRatio="xMidYMid meet"
                     v-bind:transform="'translate(' + plotMargin.left + ',' + plotMargin.top + ')'">
                    <g id="xAxis" 
                       v-bind:transform="'translate(0,' + xAxisY + ')'">
                    </g>
                    <g id="yAxis"
                       v-bind:transform="'translate(0,0)'">
                    </g>
                </svg>
            </div>
        </section>
    `
});

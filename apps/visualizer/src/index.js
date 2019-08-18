import {getHistoricalStockEodInfo} from './api.js';
import './search.js';
import './stockDisplayControl.js';
import './stockPlot.js';

import Vue from 'vue';
import Vuex, { mapActions } from 'vuex';
const moment = require('moment');

Vue.use(Vuex);

const stockStore = new Vuex.Store({
    state: {
        stocks: [],
        minDate: null,
        maxDate: null,
        minPrice: null,
        maxPrice: null
    },
    mutations: {
        addStockFinal(state, obj) {
            state.stocks.push(
                {
                    symbol: obj.symbol,
                    name: obj.name,
                    priceInfo: []
                }
            );
        },
        setPriceInfo(state, {stockIndex, priceInfo}) {
            state.stocks[stockIndex].priceInfo = priceInfo;
            for (let p of priceInfo) {
                let dt = moment(p.dateTime);
                if (!state.minDate) {
                    state.minDate = dt;
                } else {
                    state.minDate = moment.min(state.minDate, dt);
                }

                if (!state.maxDate) {
                    state.maxDate = dt;
                } else {
                    state.maxDate = moment.max(state.maxDate, dt);
                }

                if (!state.minPrice) {
                    state.minPrice = p.closePrice;
                } else {
                    state.minPrice = Math.min(state.minPrice, p.closePrice);
                }

                if (!state.maxPrice) {
                    state.maxPrice = p.closePrice;
                } else {
                    state.maxPrice = Math.max(state.maxPrice, p.closePrice);
                }

            }
        }
    },
    actions: {
        updateAllStocks({dispatch, state}) {
            for (let stock of state.stocks) {
                dispatch('updateStock', stock);
            }
        },
        async updateStock({commit, state}, {stock, stockIndex}) {
            let prices = await getHistoricalStockEodInfo(stock.symbol);
            commit('setPriceInfo', {stockIndex, priceInfo: prices});
        },
        addStock({commit, dispatch, state}, stock) {
            commit('addStockFinal', stock);
            dispatch('updateStock', {stock, stockIndex: state.stocks.length - 1});
        }
    }
});

new Vue({
    el: '#app',
    data: {
        currentDate: moment()
    },
    store: stockStore,
    computed: {
        dateTime: function () {
            return this.$data.currentDate.format('MMMM Do YYYY, h:mm:ss a');
        },
        selectedStocks: function() {
            return this.$store.state.stocks;
        }
    },
    methods: {
        ...mapActions([
            'updateAllStocks'
        ]),
    },
    template: `
    <div class="columns main">
        <!-- Navigation -->
        <div class="column is-2 primary-overlay">
            <!-- Search -->
            <section class="section">
                <stock-search></stock-search>
            </section>

            <!-- Watchlist Stocks -->
            <section class="section">
                <div class="content">
                    <p>
                        <span class="subtitle">Watchlist</span>
                        <span class="secondary-text">{{dateTime}}</span>
                    </p>
                </div>
            </section>
            <section class="section secondary-overlay">
                <stock-display-control
                     v-for="(_, index) of selectedStocks"
                     v-bind:stockIndex="index"
                     v-bind:divbg="(index % 2 == 0) ? 'secondary-bg' : 'secondary-bg-alt'">
                </stock-display-control>
            </section>
        </div>

        <!-- Primary display -->
        <div class="column is-10 primary-overlay">
            <stock-plot></stock-plot>
        </div>
    </div>`,
    created: function() {
        setInterval(() => {
            this.$data.currentDate = moment();
        }, 1000);
    }

});

import './search.js';
import './stockDisplayControl.js';

import Vue from 'vue';
import Vuex from 'vuex';
var moment = require('moment');

Vue.use(Vuex);

const stockStore = new Vuex.Store({
    state: {
        stocks: []
    },
    mutations: {
        addStock(state, obj) {
            state.stocks.push(
                {
                    symbol: obj.symbol,
                    name: obj.name,
                    priceInfo: []
                }
            );
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
                        <span class="subtitle">Watched Stocks</span>
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
            <section class="section">
            </section>
        </div>
    </div>`,
    created: function() {
        setInterval(() => {
            this.$data.currentDate = moment();
        }, 1000);
    }
});

import { library, dom } from '@fortawesome/fontawesome-svg-core';
import { faAngleDown, faSearch } from '@fortawesome/free-solid-svg-icons';


import './search.js';
import './stockDisplayControl.js';

import Vue from 'vue';
var moment = require('moment');

new Vue({
    el: '#app',
    data: {
        selectedStocks: [],
        currentDate: moment()
    },
    computed: {
        dateTime: function () {
            return this.$data.currentDate.format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    template: `
    <div class="columns main">
        <!-- Navigation -->
        <div class="column is-2 primary-overlay">
            <!-- Search -->
            <section class="section">
                <stock-search v-on:selectStock="selectedStocks.push($event)"></stock-search>
            </section>

            <!-- Active Stocks -->
            <section class="section">
                <div class="content">
                    <p>
                        <span class="subtitle">Active Stocks</span>
                        <span class="secondary-text">{{dateTime}}</span>
                    </p>
                </div>
            </section>
            <section class="section secondary-overlay">
                <stock-display-control
                     v-for="(ele, index) of selectedStocks"
                     v-bind:stock="ele"
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

library.add(faAngleDown, faSearch);
dom.watch();

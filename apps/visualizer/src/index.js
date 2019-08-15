import './search.js';
import Vue from 'vue';

new Vue({
    el: '#app',
    data: {
        selectedStocks: []
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
                <h1 class="subtitle">Active Stocks</h1>
            </section>
            <section class="section secondary-overlay">
            </section>
        </div>

        <!-- Primary display -->
        <div class="column is-10 primary-overlay">
            <section class="section">
            </section>
        </div>
    </div>`
});

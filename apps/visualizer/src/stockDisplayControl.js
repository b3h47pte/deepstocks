import Vue from 'vue';

const request = require('request');

Vue.component('stock-display-control', {
    props: ['stockIndex', 'divbg'],
    data: function() {
        return {
            showContent: false
        }
    },
    computed: {
        styleObj : function() {
            if (this.$data.showContent) {
                return {
                    display: 'block'
                }
            } else {
                return {
                    display: 'none'
                }

            }
        },
        stock: function() {
            return this.$store.state.stocks[this.$props.stockIndex];
        },
        iconRotate: function() {
            if (this.$data.showContent) {
                return '';
            } else {
                return 'fa-rotate-90';
            }
        },
        stockLastDate: function() {
            if (this.stock.priceInfo.length == 0) {
                return 'N/A';
            }
            return this.stock.priceInfo[-1].format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    methods: {
        showHideContent() {
            this.$data.showContent = !this.$data.showContent;
        }
    },
    template: `
        <div :class="[divbg, 'stock-control-card', 'card']">
            <a v-on:click="showHideContent()">
                <header class="card-header">
                    <p class="card-header-title is-6" style="display:block;">
                        <span style="display:block;">{{stock.name}} ({{stock.symbol}})</span>
                        <span style="display:block;" class="secondary-text">Last Updated: {{stockLastDate}}</span>
                    </p>
                    <a href="#" class="card-header-icon">
                        <span class="icon">
                            <i v-bind:class="['fas', 'fa-angle-down', iconRotate]"></i>
                        </span>
                    </a>
                </header>
            </a>
            <div class="card-content" v-bind:style="styleObj">
            </div>
        </div>
    `
});

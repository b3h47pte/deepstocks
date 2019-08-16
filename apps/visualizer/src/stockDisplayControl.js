import Vue from 'vue';

const request = require('request');

Vue.component('stock-display-control', {
    props: ['stockIndex', 'divbg'],
    data: function() {
        return {
            showContent: false,
            showDropdown: false,
            secondaryDataOptions: [
                {
                    name: "Moving Average",
                    add: function() {
                    }
                },
                {
                    name: "Exponential Moving Average",
                    add: function() {
                    }
                },
                {
                    name: "RSI",
                    add: function() {
                    }
                },
                {
                    name: "MACD",
                    add: function() {
                    }
                }
            ],
            currentIndex: 0
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
                    <p class="card-header-title is-6">{{stock.name}} ({{stock.symbol}})</p>
                    <a href="#" class="card-header-icon">
                        <span class="icon">
                            <i class="fas fa-angle-down" data-fa-transform="rotate-90"></i>
                        </span>
                    </a>
                </header>
            </a>
            <div class="card-content" v-bind:style="styleObj">
                <div class="primary-display-control-wrapper">
                    <div>
                        <input type="checkbox" id="showPrice" v-model="stock.display.showPrice"><label for="showPrice" class="primary-text-control">Price</label>
                    </div>
                    <div>
                        <input type="checkbox" id="showCandlesticks" v-model="stock.display.showCandlesticks"><label for="showCandlesticks" class="primary-text-control">Candlesticks</label>
                    </div>
                    <div>
                        <input type="checkbox" id="showVolume" v-model="stock.display.showVolume"><label for="showVolume" class="primary-text-control">Volume</label>
                    </div>
                </div>
                <hr>
                <div class="dropdown" v-bind:class="{'is-active': showDropdown}">
                    <button class="button"
                            v-on:click="showDropdown = !showDropdown"
                            v-on:focusout="showDropdown = false">
                        <span class="icon">
                            <i class="fas fa-plus"></i>
                        </span>
                        <span>Add Secondary Data</span>
                    </button>
                    <div class="dropdown-menu">
                        <div class="dropdown-content">
                            <a href="#"
                               class ="dropdown-item"
                               v-for="(ele, index) of secondaryDataOptions"
                               v-bind:class="{'on-item-hover' : index == currentIndex}"
                               v-on:mouseover="currentIndex = index"
                               v-on:click="ele.add()">
                                {{ele.name}}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
});

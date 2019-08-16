import Vue from 'vue';

const request = require('request');

Vue.component('stock-display-control', {
    props: ['stock', 'divbg'],
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
            </div>
        </div>
    `
});
